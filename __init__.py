# TODO: Add an appropriate license to your skill before publishing.  See
# the LICENSE file for more information.

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import getLogger
import re

class SplitterSkill(MycroftSkill):

    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        super(SplitterSkill, self).__init__(name="SplitterSkill")



        # Initialize working variables used within the skill.

    @intent_handler(IntentBuilder("").require("Split").require("Word"))
    def handle_split_word_intent(self, message):
        suffixRegex  = re.compile(r'(s$)|(ed$)|(ation$)')
        prefixRegex = re.compile(r'(^pre)')
        suffix = ""
        prefix = ""
        rootword = ""

        def splitSuffix(toSplit_):
            suffixMatch = suffixRegex.search(toSplit_)
            if suffixMatch:
                suffix = suffixMatch.group(0)
                rootword = toSplit_[:suffixMatch.start(0)]
            else:
                suffix = "None"
                rootword = toSplit_

        def splitPrefix(toSplit_):
            prefixMatch = prefixRegex.search(toSplit_)
            if prefixMatch:
                prefix = prefixMatch.group(0)
            else:
                prefix = "None"

        toSplit = message.data.get("Word")
        suffixMatch = suffixRegex.search(toSplit)
        if suffixMatch:
            suffix = suffixMatch.group(0)
            # First strip out suffixes
            rootword = toSplit_[:suffixMatch.start(0)]
        else:
            suffix = "None"
            rootword = toSplit

        prefixMatch = prefixRegex.search(rootword)
        # Then strip out prefixes
        if prefixMatch:
            prefix = prefixMatch.group(0)
            rootword = rootword[prefixMatch.end(0):]
        else:
            prefix = "None"

        self.speak_dialog("rootword", data={"word": toSplit, "rootword": rootword})
        self.speak_dialog("suffix", data={"suffix": suffix})
        self.speak_dialog("prefix", data={"prefix": prefix})

    @intent_handler(IntentBuilder("").require("Pluralize").require("Word"))
    def handle_pluralize_word_intent(self, message):

        def pluralize_word(toPluralize_):
            if (re.search('[Zz]$', toPluralize_)):
                pluralizedWord_ = toPluralize_ + "es"
                return pluralizedWord_
            else:
                pluralizedWord_ = toPluralize_ + "s"
                return pluralizedWord_

        toPluralize = message.data["Word"]
        pluralizedWord = pluralize_word(toPluralize)
        self.speak_dialog("pluralize", data={"toPluralize": toPluralize, "pluralizedWord": pluralizedWord})


    # def stop(self):
    #    return False

# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    return SplitterSkill()
