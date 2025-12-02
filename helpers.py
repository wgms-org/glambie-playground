"""Helper constants, functions, and command line interface."""
import datetime
import os
from pathlib import Path

import dotenv
import fire
from getfilelistpy import getfilelist
import requests


# ---- Constants ----

# Load environment variables from .env file to os.environ
dotenv.load_dotenv()

DATA_PATH: Path = Path('data')
"""Path to the data directory."""

GOOGLE_DRIVE_CONVERSIONS: dict[str, tuple[str, str]] = {
  'application/vnd.google-apps.document': (
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'docx'
  ),
  'application/vnd.google-apps.spreadsheet': (
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'xlsx'
  ),
  'application/vnd.google-apps.presentation': (
    'application/vnd.openxmlformats-officedocument.presentationml.presentation', 'pptx'
  ),
}
"""Mapping of Google Drive MIME types to export MIME types and file extensions."""


# ---- Functions ----

def hello_world() -> str:
  """Greet the world."""
  return 'Hello, world!'


def download_data() -> None:
  """
  Download all files in the shared Google Drive folder to the local data directory.

  Native Google Drive files are converted to the following formats:

  * Google Docs: .docx (Word)
  * Google Sheets: .xlsx (Excel)
  * Google Slides: .pptx (PowerPoint)

  Existing files are skipped unless the remote file has since been modified or
  (for files that are not converted) the file size differs.
  """
  if (
    not os.environ.get('GOOGLE_DRIVE_FOLDER_ID') or
    not os.environ.get('GOOGLE_DRIVE_API_KEY')
  ):
    raise ValueError(
      'Environment variables (GOOGLE_DRIVE_FOLDER_ID, GOOGLE_DRIVE_API_KEY)'
      ' missing from .env file.'
      ' See README.md for installation instructions.'
    )
  remote_folders = getfilelist.GetFileList({
    'api_key': os.environ['GOOGLE_DRIVE_API_KEY'],
    'id': os.environ['GOOGLE_DRIVE_FOLDER_ID']
  })
  DATA_PATH.mkdir(exist_ok=True)
  remote_folder_names = {fid: name for fid, name in zip(
    remote_folders['folderTree']['folders'][1:],
    remote_folders['folderTree']['names'][1:]
  )}
  for remote_folder in remote_folders['fileList']:
    remote_folder_path = Path(
      *[remote_folder_names[fid] for fid in remote_folder['folderTree'][1:]]
    )
    folder_path = DATA_PATH / remote_folder_path
    folder_path.mkdir(parents=True, exist_ok=True)
    for remote_file in remote_folder['files']:
      file_path: Path = folder_path / remote_file['name']
      conversion = False
      if remote_file['mimeType'] in GOOGLE_DRIVE_CONVERSIONS:
        # Convert Google Drive files to a format that can be opened locally
        mime_type, file_extension = GOOGLE_DRIVE_CONVERSIONS[remote_file['mimeType']]
        url = f"https://www.googleapis.com/drive/v3/files/{remote_file['id']}/export"
        params = {'mimeType': mime_type, 'key': os.environ['GOOGLE_DRIVE_API_KEY']}
        file_path = file_path.with_suffix(f'.{file_extension}')
        conversion = True
      else:
        url = f"https://www.googleapis.com/drive/v3/files/{remote_file['id']}"
        params = {'alt': 'media', 'key': os.environ['GOOGLE_DRIVE_API_KEY']}
      # Skip download if an existing file matches the remote file
      remote_file_size = int(remote_file['size'])
      remote_file_modified = datetime.datetime.fromisoformat(remote_file['modifiedTime'])
      if file_path.exists():
        file_size = file_path.stat().st_size
        file_modified = datetime.datetime.fromtimestamp(
          file_path.stat().st_mtime, tz=datetime.timezone.utc
        )
        if (
          (remote_file_modified - file_modified) <= datetime.timedelta(seconds=1) and
          (conversion or remote_file_size == file_size)
        ):
          print('[SKIP]', file_path)
          continue
        else:
          print('[UPDATE]', file_path)
      else:
        print('[CREATE]', file_path)
      response = requests.get(url=url, params=params)
      with open(file_path, 'wb') as file_buffer:
        file_buffer.write(response.content)
      # Set file modification time to match remote file on next update
      modified_seconds = remote_file_modified.timestamp()
      os.utime(file_path, times=(modified_seconds, modified_seconds))


# ---- Command Line Interface ----

if __name__ == '__main__':
  # Add functions here to make them callable from the command line
  fire.Fire({
    'hello_world': hello_world,
    'download_data': download_data,
  })
