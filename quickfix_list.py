from __future__ import division
import sublime, sublime_plugin
import os

# import traceback


QuickFix_CurrentLine = -1

# TODO:
# hotkeys: next, prev, copen, cfirst
# commands: next, prev, open file
# support
# multiple delimiters(:,|)
# pick vim quickfix file by default or configurable
# TODO add vim and fzf snippets & even include a gif. Create a Medium.com blog too
# error handling if match is not valid anymore, if tmp file is not available

settings_path = "QuickfixList.sublime-settings"


class QuickfixList(sublime_plugin.TextCommand):
    def run(self, edit, action="next", next=True):
        self.settings = sublime.load_settings(settings_path)
        QUICKFIX_CUSTOM_FILE = self.settings.get(
            "QUICKFIX_CUSTOM_FILE", "/tmp/sublime_quickfix_list.txt"
        )
        global QuickFix_CurrentLine

        if action in ["next", "prev"]:

            with open(QUICKFIX_CUSTOM_FILE) as f:
                txt = f.read()
                inc = 1 if action == "next" else -1
                QuickFix_CurrentLine += inc
                QuickFix_CurrentLine = (
                    0
                    if QuickFix_CurrentLine >= len(txt.splitlines())
                    else QuickFix_CurrentLine
                )
                filename = txt.splitlines()[QuickFix_CurrentLine].strip()
                # open_filepaths(self, clean_filepath(filename))
                # TODO add try catch
                file_path=filename.split(":")[0]
                line_num=filename.split(":")[1]
                if os.path.isfile(file_path):
                    print("Opening file_path '%s'" % (file_path))
                    self.view.window().open_file("{0}:{1}".format(file_path,line_num), sublime.ENCODED_POSITION)

                else:
                    print("No filename discovered")
        elif action == "open":
            # TODO open at current active match
            self.view.window().open_file(QUICKFIX_CUSTOM_FILE, sublime.ENCODED_POSITION)
