import threading
import urllib.parse
import requests
import re
import os


class TellyEngine:
    request = None

    def __init__(self, url, directory, tag, identifier, process_id):
        self.link = r'{}'.format(urllib.parse.unquote(url))
        self.directory = directory
        self.tag = tag
        self.identifier = identifier
        self.pid = process_id

        self.request_it()

    def request_it(self):
        try:
            request = requests.get(self.link, stream=True, allow_redirects=True)
        except Exception as e:
            str(e.args)
            request = None
        self.request = request

    def confirm_existence(self):
        if not self.request:
            return False
        elif self.request:
            return True

    def get_name(self):
        if self.confirm_existence():
            if "Content-Disposition" in self.request.headers.keys():
                name = re.findall("filename=\"(.+)\"", self.request.headers["Content-Disposition"])[0]
            else:
                name = self.link.split("/")[-1]
            name = name.split("?")[0]
            return name
        if not self.confirm_existence():
            name = "Failure: Error NM101.telly"
            return name

    def get_size(self):
        if self.confirm_existence():
            total_size = self.request.headers["Content-Length"]
            return int(total_size)
        elif not self.confirm_existence():
            total_size = 1
            return total_size

    def get_media(self):
        if self.confirm_existence():
            media = self.request.headers["Content-Type"]
            return media
        elif not self.confirm_existence():
            media = "unrecognized"
            return media

    def get_file_extension(self):
        file_extension = self.get_name().split(".")[-1]
        return file_extension

    def get_error_file(self):
        error_file = "Libraries/Temps/" + self.pid + self.tag + self.identifier + ".tef"
        return error_file

    def stop_download(self, state):
        with open(self.get_error_file(), "w") as f:
            f.write("state = " + state)

    def get_tag(self):
        return self.tag

    def get_identifier(self):
        return self.identifier

    def get_process_identifier(self):
        return self.pid

    def get_url(self):
        return self.link

    def get_directory(self):
        return self.directory

    def get_file_location_name(self):
        return self.get_directory() + "/" + self.get_name()

    def prep_resume_download(self):
        if os.path.exists(self.get_file_location_name()):
            size_now = os.path.getsize(self.get_file_location_name())
            header = {'Range': 'bytes=%d-' % size_now}

            with requests.get(self.link, stream=True, allow_redirects=True, headers=header, timeout=None) as r:
                with open(self.get_file_location_name(), 'ab') as f:
                    for chunk in r.iter_content(chunk_size=1024):
                        if not os.path.exists(self.get_error_file()):
                            if chunk:
                                f.write(chunk)
                        else:
                            break

    def resume_download(self):
        threading.Thread(target=lambda: self.prep_resume_download()).start()

    def prep_download(self):
        with requests.get(self.link, stream=True, allow_redirects=True, timeout=5) as r:
            with open(self.get_file_location_name(), 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if not os.path.exists(self.get_error_file()):
                        if chunk:
                            f.write(chunk)
                    else:
                        break

    def download_file(self):
        threading.Thread(target=lambda: self.prep_download()).start()
