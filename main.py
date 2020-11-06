from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import difflib
import json

Builder.load_file('design.kv') #To connect to .kv file

data = json.load(open('data.json'))

class Screen1(Screen):

    def search_definition(self, word):
        if word in data:
            self.ids.definition_list.text = str(data[word]).replace("['", "-").replace("']", "").replace("', '", "\n-")
        elif word.lower() in data:
            self.ids.definition_list.text = str(data[word.lower()]).replace("['", "-").replace("']", "").replace("', '", "\n-")
        elif word.title() in data:
            self.ids.definition_list.text = str(data[word.title()]).replace("['", "-").replace("']", "").replace("', '", "\n-")
        elif word.upper() in data:
            self.ids.definition_list.text = str(data[word.upper()]).replace("['", "-").replace("']", "").replace("', '", "\n-")
        else:
            try:
                alternative_word = [difflib.get_close_matches(word, data, n=1)]
                word_alternate = str(alternative_word[0]).replace("['", "").replace("']", "")
                list = data[word_alternate] #creates new list to avoid writing to the database
                list.insert(0, "Did you mean " + word_alternate + "?")
                self.ids.definition_list.text = str(data[word_alternate]).replace("['", " ").replace("']", "").replace("', '", "\n-")
                print(self.ids.definition_list.text)
                print(type(self.ids.definition_list.text))
            except KeyError:
                self.ids.definition_list.text = "That word is not available in this dictionary. Check your spelling."


    def clear(self, not_word):
        self.ids.word_to_look.text = " "
        self.ids.definition_list.text = " "


class RootWidget(ScreenManager):
    pass

class DictionaryApp(App):
    def build(self):
        return RootWidget() #obj, not class

if __name__ == "__main__":
    DictionaryApp().run()