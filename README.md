# Automate some stuff

![Image](https://www.ntaskmanager.com/wp-content/uploads/2021/01/Benefits-of-task-automation-700x280.png)

> This is a collection of scripts to automate your drive
> > Uploading files to drive
> 
> > Downloading files from drive
> 
> > Deleting files from drive
> 
> > Creating folders in drive
> 
> > Deleting folders in drive
> 
> > Moving files in drive
> 
> > Moving folders in drive
> 
> > Uploading entire directories to drive
> 
> > Searching for files in drive
> 
> > Searching for folders in drive

---

## Before you start
please read this article first: [How to use pydrive](https://pythonhosted.org/PyDrive/)

You will also need to get a gcp account and create a project and enable the drive api
Here a link on how to do that: [How to enable drive api](https://developers.google.com/drive/api/v3/quickstart/python)

> Once you have done that, you will need to download the credentials.json file and place it in the same directory as the test script (example: in the samples folder where the test.py file is)

> You can also create a settings.yaml file and place it in the same directory as the MyDrive.py file (optional)

Example of settings.yaml file:
    
    
    client_config_backend: settings
    client_config:
      client_id: "your client id here"
      client_secret: "your client secret here"
    save_credentials: True
    save_credentials_backend: file
    save_credentials_file: mycredentials.json

    get_refresh_token: True

    oauth_scope:
      - https://www.googleapis.com/auth/drive.file
      - https://www.googleapis.com/auth/drive.metadata.readonly
      - https://www.googleapis.com/auth/drive.appdata
      - https://www.googleapis.com/auth/drive.install

---
## How to use

1. Clone the repo
2. Install the requirements (pip install -r requirements.txt)
3. create your own script and import the functions you need
4. Dont forget to add the credentials.json (renamed to **client_secrets**) file in the same directory as your script
5. Run your script
6. Enjoy


