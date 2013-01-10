import re
import logging
import functools
import copy
import unittest
import bigfont
import smoosh

class BigLetter(bigfont.base.BaseObject):
    """
    Represents a single letter in a font.
    """
    
    def __init__(self,lines,hardblank='$',rules=None,**kwargs):
        super().__init__(**kwargs)
        self._set_lines(lines)
        self.hardblank = hardblank
        if rules is None:
            self.rules = smoosh.Smoosher()
        else:
            self.rules = rules

    def _set_lines(self,lines):
        self.lines = list(lines)
        self.height = len(lines)
        self.maxwidth = functools.reduce(max,[len(line) for line in lines])    

    def __str__(self):
        out = "\n".join(self.lines)
        return re.sub(re.escape(self.hardblank),' ',out) # remove hardblanks

    def __add__(self,other):
        #fixme use smoosh rules
        newlines = []
        for s,o in zip(self.lines, other.lines):
            newlines.append(s + o)
        newletter = copy.copy(self)
        newletter._set_lines(newlines)
        return newletter

    def __eq__(self,other):
        if self.lines == other.lines:
            return True
        return False

    def __iadd__(self,other):
        newlines = []
        for s,o in zip(self.lines, other.lines):
            newlines.append(s + o)
        self._set_lines(newlines)
        return self

    def __iter__(self):
        for line in self.lines:
            yield line

    def touch(self,other):
        """Determine this letter touches other letter on its right side."""
        for lr,rr in zip(self,other):
            if lr[-1] != ' ' and rr[0] != ' ':
                return True
        return False

    def horizontal_space(self,other):
        """Returns the smallest amount of horizontal space between
        this letter's right side and another letter."""
        minspace = None
        for lrow,rrow in zip(self,other):
            ls = lrow.rstrip(' ')
            rs = rrow.lstrip(' ')
            lstripped = len(lrow) - len(ls)
            rstripped = len(rrow) - len(rs)
            separation = lstripped + rstripped
            if minspace is None or separation < minspace:
                minspace = separation
        return minspace

    def kern(self,other):
        """Overlap two letters until they touch."""
        overlap = self.horizontal_space(other)
        return self.push(other,overlap=overlap)    

    def push(self,other,overlap=1):
        """Push two letters together into a new one."""
        newlines = []
        for s,o in zip(self.lines, other.lines):
            leftchars = s[:-overlap]
            rightchars = o[overlap:]
            leftoverlap = s[-overlap:]
            rightoverlap = o[:overlap]
            overlapped = self.rules.smoosh(leftoverlap,rightoverlap)
            newlines.append(leftchars + overlapped + rightchars)
        newletter = copy.copy(self)
        newletter._set_lines(newlines)
        return newletter           
    
class BasicBigLetterTests(unittest.TestCase):

    def setUp(self):
        self.letterD = BigLetter(["|-\\","| |","| /"])
        self.letterE = BigLetter(("----","--  ","____"))
        #print(self.letterD)
        #print(self.letterE)

    def test_add(self):
        dc = copy.copy(self.letterD)
        de = self.letterD + self.letterE
        de2 = copy.copy(self.letterD)
        de2 += self.letterE
        self.assertEqual(de, de2)
        self.assertEqual(dc + self.letterD, self.letterD + dc)

    def test_equality(self):
        self.assertNotEqual(self.letterD,self.letterE)
        self.assertEqual(copy.copy(self.letterD),self.letterD)
        

if __name__ == "__main__":
    unittest.main(exit=False)
