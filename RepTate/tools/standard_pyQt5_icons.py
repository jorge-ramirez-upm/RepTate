import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
 
class Widget(QWidget):
     
    def __init__(self, parent= None):
        super(Widget, self).__init__()
 
        icons = [
            'SP_ArrowBack',
            'SP_ArrowDown',
            'SP_ArrowForward',
            'SP_ArrowLeft',
            'SP_ArrowRight',
            'SP_ArrowUp',
            'SP_BrowserReload',
            'SP_BrowserStop',
            'SP_CommandLink',
            'SP_ComputerIcon',
            'SP_CustomBase',
            'SP_DesktopIcon',
            'SP_DialogApplyButton',
            'SP_DialogCancelButton',
            'SP_DialogCloseButton',
            'SP_DialogDiscardButton',
            'SP_DialogHelpButton',
            'SP_DialogNoButton',
            'SP_DialogOkButton',
            'SP_DialogOpenButton',
            'SP_DialogResetButton',
            'SP_DialogSaveButton',
            'SP_DialogYesButton',
            'SP_DirClosedIcon',
            'SP_DirHomeIcon',
            'SP_DirIcon',
            'SP_DirLinkIcon',
            'SP_DirOpenIcon',
            'SP_DockWidgetCloseButton',
            'SP_DriveCDIcon',
            'SP_DriveDVDIcon',
            'SP_DriveFDIcon',
            'SP_DriveHDIcon',
            'SP_DriveNetIcon',
            'SP_FileDialogBack',
            'SP_FileDialogContentsView',
            'SP_FileDialogDetailedView',
            'SP_FileDialogEnd',
            'SP_FileDialogInfoView',
            'SP_FileDialogListView',
            'SP_FileDialogNewFolder',
            'SP_FileDialogStart',
            'SP_FileDialogToParent',
            'SP_FileIcon',
            'SP_FileLinkIcon',
            'SP_MediaPause',
            'SP_MediaPlay',
            'SP_MediaSeekBackward',
            'SP_MediaSeekForward',
            'SP_MediaSkipBackward',
            'SP_MediaSkipForward',
            'SP_MediaStop',
            'SP_MediaVolume',
            'SP_MediaVolumeMuted',
            'SP_MessageBoxCritical',
            'SP_MessageBoxInformation',
            'SP_MessageBoxQuestion',
            'SP_MessageBoxWarning',
            'SP_TitleBarCloseButton',
            'SP_TitleBarContextHelpButton',
            'SP_TitleBarMaxButton',
            'SP_TitleBarMenuButton',
            'SP_TitleBarMinButton',
            'SP_TitleBarNormalButton',
            'SP_TitleBarShadeButton',
            'SP_TitleBarUnshadeButton',
            'SP_ToolBarHorizontalExtensionButton',
            'SP_ToolBarVerticalExtensionButton',
            'SP_TrashIcon',
            'SP_VistaShield'
            ]
 
        colSize = 4
         
        layout = QGridLayout()
 
        count = 0
        for i in icons:
            btn = QPushButton(i)
            btn.setIcon(self.style().standardIcon(getattr(QStyle, i)))
 
            layout.addWidget(btn, count / colSize, count % colSize)
            count += 1
             
        self.setLayout(layout)
         
if __name__ == '__main__':
    app = QApplication(sys.argv)
             
    dialog = Widget()
    dialog.show()
             
    app.exec_()