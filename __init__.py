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

    # ISOLATES AND STRIPS PREFIXES AND SUFFIXES
    @intent_handler(IntentBuilder("").require("Split").require("Word"))
    def handle_split_word_intent(self, message):
        suffixRegex  = re.compile(r'(s$)|(ion$)|(acy$)|(al$)|(dom$)|(er$)|(ify$)|(ism$)|(ist$)|(ity$)|(ness$)|(ship$)|(ment$)|(ly$)')
        prefixRegex = re.compile(r'(^pre)|(^post)|(^anti)|(^auto)|(^co)|(^contra)|(^de)|(^dis)|(^hyper)|(^micro)|(^macro)')
        suffix = ""
        prefix = ""
        rootword = ""

        toSplit = message.data.get("Word")
        suffixMatch = suffixRegex.search(toSplit)
        if suffixMatch:
            suffix = suffixMatch.group(0)
            # First strip out suffixes
            rootword = toSplit[:suffixMatch.start(0)]
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
        if suffix != "None":
            self.speak_dialog("suffix", data={"suffix": suffix})
        if prefix != "None":
            self.speak_dialog("prefix", data={"prefix": prefix})

    # PLURALIZES A WORD
    @intent_handler(IntentBuilder("").require("Pluralize").require("Word"))
    def handle_pluralize_word_intent(self, message):
        esRegex = re.compile(r'[zs]$')

        def pluralize_word(toPluralize_):
            if esRegex.search(toPluralize_):
                pluralizedWord_ = toPluralize_ + "es"
                return pluralizedWord_
            else:
                pluralizedWord_ = toPluralize_ + "s"
                return pluralizedWord_

        toPluralize = message.data.get("Word")
        pluralizedWord = pluralize_word(toPluralize)
        self.speak_dialog("pluralize", data={"toPluralize": toPluralize, "pluralizedWord": pluralizedWord})


    # PUTS A WORD INTO PAST TENSE
    @intent_handler(IntentBuilder("").require("Word").require("Past"))
    def handle_pasttense_word_intent(self, message):
        eRegex = re.compile(r'[e]$')

        def pasttense_word(toPastTense_):
            if eRegex.search(toPastTense_):
                pastTensedWord_ = toPastTense_ + "d"
                return pastTensedWord_
            else:
                pastTensedWord_ = toPastTense_ + "ed"
                return pastTensedWord_

        toPastTense = message.data.get("Word")
        pastTensedWord = pasttense_word(toPastTense)
        self.speak_dialog("pasttense", data={"toPastTense":toPastTense, "pastTensedWord": pastTensedWord})

    # def stop(self):
    #    return False

# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    return SplitterSkill()
