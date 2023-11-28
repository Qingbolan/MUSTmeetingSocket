#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# import PyQt5 as PyQt
pyQtVersion = "PyQt5"
from PyQt5.QtCore import Qt, QRect, QRegExp
from PyQt5.QtWidgets import QWidget
from qfluentwidgets import TextEdit, PlainTextEdit
from PyQt5.QtGui import (QColor, QPainter, QFont, QSyntaxHighlighter,
                        QTextFormat, QTextCharFormat, QPen) 
from ..common.config import cfg
from clang.cindex import Index, TranslationUnit, TokenKind, Diagnostic

# classes definition
class CppHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(CppHighlighter, self).__init__(parent)
        
    def highlightBlock(self, text):
        index = Index.create()
        tu = TranslationUnit.from_source('tmp.cpp', ['-x', 'c++', '-std=c++11', '-I','E:\\develop\\CorCpp\\cygwin\\usr\\i686-w64-mingw32\\sys-root\\mingw\\include'], unsaved_files=[('tmp.cpp', text)])
        # 统一使用一种现代、科技风格的字体
        fontFamily = "Consolas"
        
        # 关键字格式
        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(QColor("#81A2BE"))  # 科技蓝
        keywordFormat.setFontWeight(QFont.Bold)  # 加粗
        keywordFormat.setFontFamily(fontFamily)
        
        # 注释格式
        commentFormat = QTextCharFormat()
        commentFormat.setForeground(QColor("#B5BD68"))  # 科技绿
        commentFormat.setFontItalic(True)  # 斜体
        commentFormat.setFontFamily(fontFamily)
        
        # 字面量格式
        literalFormat = QTextCharFormat()
        literalFormat.setForeground(QColor("#CC6666"))  # 科技红
        literalFormat.setFontFamily(fontFamily)
        
        # 标识符格式
        identifierFormat = QTextCharFormat()
        identifierFormat.setForeground(QColor("#DE935F"))  # 科技橙
        identifierFormat.setFontFamily(fontFamily)
        
        # 标点符号格式
        punctuationFormat = QTextCharFormat()
        punctuationFormat.setForeground(QColor("#C5C8C6"))  # 科技灰
        punctuationFormat.setFontFamily(fontFamily)
        
        # 预处理器格式
        preprocessorFormat = QTextCharFormat()
        preprocessorFormat.setForeground(QColor("#F0C674"))  # 科技黄
        preprocessorFormat.setFontFamily(fontFamily)

        for token in tu.get_tokens(extent=tu.cursor.extent):
            format_to_use = None  # 默认没有格式
            if token.kind == TokenKind.KEYWORD:
                format_to_use = keywordFormat
            elif token.kind == TokenKind.COMMENT:
                format_to_use = commentFormat
            elif token.kind == TokenKind.LITERAL:
                format_to_use = literalFormat
            elif token.kind == TokenKind.IDENTIFIER or token.kind == TokenKind.PUNCTUATION:
                format_to_use = identifierFormat
            elif token.kind == TokenKind.PUNCTUATION:
                format_to_use = punctuationFormat
            elif token.kind == TokenKind.PREPROCESSOR:
                format_to_use = preprocessorFormat
            
            # 应用格式
            if format_to_use:
                self.setFormat(token.extent.start.column - 1, len(token.spelling), format_to_use)
        
        fontFamily = "Consolas"
        
        errorFormat = QTextCharFormat()
        errorFormat.setUnderlineColor(QColor("#FF0000"))  # 红色
        errorFormat.setUnderlineStyle(QTextCharFormat.WaveUnderline)
        errorFormat.setFontFamily(fontFamily)
        errorFormat.setFontWeight(QFont.Bold)
        errorFormat.setForeground(QColor("#FF0000"))  # 红色

        # Handle Diagnostics
        for diag in tu.diagnostics:
            if diag.severity in [Diagnostic.Warning, Diagnostic.Error, Diagnostic.Fatal]:
                print(diag.spelling)
                start_offset = diag.location.offset
                end_offset = start_offset + len(diag.spelling)
                self.setFormat(start_offset, end_offset - start_offset, errorFormat)


class QCodeEditor(PlainTextEdit):
    class NumberBar(QWidget):
        '''class that deifnes textEditor numberBar'''

        themeColor = cfg.get(cfg.themeColor)

        def __init__(self, editor):
            QWidget.__init__(self, editor)
            
            self.editor = editor
            self.editor.blockCountChanged.connect(self.updateWidth)
            self.editor.updateRequest.connect(self.updateContents)
            self.font = QFont()
            # self.numberBarColor = cfg.themeColor
            # print("themeColor: ", cfg.themeColor,"type: ", type(cfg.themeColor))
            self.updateWidth()
                     
        def paintEvent(self, event):
            
            painter = QPainter(self)
            # painter.fillRect(event.rect(), self.numberBarColor)
             
            block = self.editor.firstVisibleBlock()
 
            # Iterate over all visible text blocks in the document.
            while block.isValid():
                blockNumber = block.blockNumber()
                block_top = self.editor.blockBoundingGeometry(block).translated(self.editor.contentOffset()).top()
 
                # Check if the position of the block is out side of the visible area.
                if not block.isVisible() or block_top >= event.rect().bottom():
                    break
 
                # We want the line number for the selected line to be bold.
                if blockNumber == self.editor.textCursor().blockNumber():
                    self.font.setBold(True)
                    # painter.setPen(QColor("#000000"))
                    # print(cfg.get(cfg.themeColor))
                    color = self.themeColor
                    painter.setPen(color)
                else:
                    self.font.setBold(False)
                    painter.setPen(QColor("#717171"))
                painter.setFont(self.font)
                
                # Draw the line number right justified at the position of the line.
                # paint_rect = QRect(0, int(block_top), int(self.width()), int(self.editor.fontMetrics().height()))
                # 获取绘制矩形的坐标和大小
                paint_rect = QRect(0, int(block_top), int(self.width()), int(self.editor.fontMetrics().height()))
                
                painter.drawText(paint_rect, Qt.AlignRight, str(blockNumber+1))
 
                block = block.next()
 
            painter.end()
            
            QWidget.paintEvent(self, event)
 
        def getWidth(self):
            count = self.editor.blockCount()
            width = self.fontMetrics().width(str(count)) + 10
            return width      
        
        def updateWidth(self):
            width = self.getWidth()
            if self.width() != width:
                self.setFixedWidth(width)
                self.editor.setViewportMargins(width, 0, 0, 0)
 
        def updateContents(self, rect, scroll):
            if scroll:
                self.scroll(0, scroll)
            else:
                self.update(0, rect.y(), self.width(), rect.height())
            
            if rect.contains(self.editor.viewport().rect()):   
                fontSize = self.editor.currentCharFormat().font().pointSize()
                self.font.setPointSize(fontSize)
                self.font.setStyle(QFont.StyleNormal)
                self.updateWidth()
                
        
    def __init__(self, DISPLAY_LINE_NUMBERS=True, HIGHLIGHT_CURRENT_LINE=True,
                 SyntaxHighlighter=None, *args):                       
        super(QCodeEditor, self).__init__()
        
        self.setFont(QFont("Ubuntu Mono", 11))
        self.setLineWrapMode(PlainTextEdit.NoWrap)
                               
        self.DISPLAY_LINE_NUMBERS = DISPLAY_LINE_NUMBERS

        if DISPLAY_LINE_NUMBERS:
            self.number_bar = self.NumberBar(self)
            
        if HIGHLIGHT_CURRENT_LINE:
            self.currentLineNumber = None
            # self.currentLineColor = self.palette().alternateBase()
            self.currentLineColor =  cfg.get(cfg.themeColor)
            self.cursorPositionChanged.connect(self.highligtCurrentLine)
        
        if SyntaxHighlighter is not None: # add highlighter to textdocument
           self.highlighter = SyntaxHighlighter(self.document())         
                 
    def resizeEvent(self, *e):
        '''overload resizeEvent handler'''
                
        if self.DISPLAY_LINE_NUMBERS:   # resize number_bar widget
            cr = self.contentsRect()
            rec = QRect(cr.left(), cr.top(), self.number_bar.getWidth(), cr.height())
            self.number_bar.setGeometry(rec)
        
        PlainTextEdit.resizeEvent(self, *e)

    def highligtCurrentLine(self):
        newCurrentLineNumber = self.textCursor().blockNumber()
        if newCurrentLineNumber != self.currentLineNumber:                
            self.currentLineNumber = newCurrentLineNumber
            hi_selection = TextEdit.ExtraSelection() 
            hi_selection.format.setBackground(self.currentLineColor)
            hi_selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            hi_selection.cursor = self.textCursor()
            hi_selection.cursor.clearSelection() 
            self.setExtraSelections([hi_selection])           

##############################################################################
         
if __name__ == '__main__':

    # TESTING        
    
    def run_test():
    
        print("\n {} is imported".format(pyQtVersion))
        # imports requied PyQt modules
        from PyQt5.QtWidgets import QApplication
        
        import sys
       
        app = QApplication([])
        
        editor = QCodeEditor(DISPLAY_LINE_NUMBERS=True, 
                             HIGHLIGHT_CURRENT_LINE=True,
                             SyntaxHighlighter=CppHighlighter)
        
        text = '''<FINITELATTICE>
  <LATTICE name="myLattice">
    <BASIS>
      <VECTOR>1.0 0.0 0.0</VECTOR>
      <VECTOR>0.0 1.0 0.0</VECTOR>
    </BASIS>
  </LATTICE>
  <PARAMETER name="L" />
  <PARAMETER default="L" name="W" />
  <EXTENT dimension="1" size="L" />
  <EXTENT dimension="2" size="W" />
  <BOUNDARY type="periodic" />
</FINITELATTICE>
'''
        editor.setPlainText(text)
        editor.resize(400,250)
        editor.show()
    
        sys.exit(app.exec_())

    
    run_test()
