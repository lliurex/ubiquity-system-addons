# -*- coding: utf-8; Mode: Python; indent-tabs-mode: nil; tab-width: 4 -*-

from ubiquity import misc, plugin, validation
import os
import inspect
import gettext


NAME = 'lliurexSystemAddons'
AFTER = 'lliurexExtrapackages'
BEFORE = 'usersetup'
WEIGHT = 40


gettext.textdomain('ubilliurexdesktoplayout')
_ = gettext.gettext

class PageKde(plugin.PluginUI):
    plugin_title = 'lliurex/text/breadcrumb_systemAddons'
    plugin_breadcrumb = 'lliurex/text/breadcrumb_systemAddons'
    plugin_prefix = 'lliurex/text'
    
    def __init__(self, controller, *args, **kwargs):
        from PyQt5.QtGui import QPixmap, QIcon, QFont
        from PyQt5.QtWidgets import QWidget, QFrame, QVBoxLayout, QScrollArea, QGridLayout, QHBoxLayout, QLabel, QSizePolicy, QRadioButton
        from PyQt5.QtCore import Qt
        self.configuration = {'flash':True,'statistics':True}
        self.controller = controller
        self.main_widget = QFrame()
        self.translations = {"flashname":"Flash support", "flashdescription": "Install Flash package", "statisticsname" : "Statistics usage","statisticsdescription" : "Send anonymous statistics usage to improve LliureX"}

        self.main_widget.setLayout(QVBoxLayout())
        qsa = QScrollArea()
        widget = QWidget()
        widget.setLayout(QVBoxLayout())
        widget.layout().setAlignment(Qt.AlignCenter | Qt.AlignTop)
        qsa.setWidget(widget)
        qsa.setWidgetResizable(True)

        self.main_widget.layout().addWidget(qsa)

        widget.layout().addLayout(self.createFlash(False),False)
        widget.layout().addLayout(self.createStatistics(True),True)

        self.page = widget
        self.plugin_widgets = self.page


    def createFlash(self,last):
        from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QVBoxLayout
        from PyQt5.QtCore import Qt

        gLayout = QGridLayout()
        horizontalLayout = QHBoxLayout()
        horizontalLayout.setObjectName("horizontalLayout")
        verticalLayout = QVBoxLayout()
        verticalLayout.setObjectName("verticalLayout")
        horizontalLayout.addLayout(verticalLayout)

        image_package = self.createImage(os.path.join('/usr/share/ubiquity-system-addons','flash.svg'))
        self.flash_name_package = self.createName(_(self.translations['flashname']))
        self.flash_description_package = self.createDescription(_(self.translations['flashdescription']))
        install_package = self.createCheck('flash')

        verticalLayout.addWidget(self.flash_name_package)
        verticalLayout.addWidget(self.flash_description_package)
        verticalLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        verticalLayout.setContentsMargins(10,20,0,0)
        horizontalLayout.addWidget(install_package)

        gLayout.addWidget(image_package,0,0)
        gLayout.addLayout(horizontalLayout,0,1)
        gLayout.addLayout(self.add_line(),1,1)
        return gLayout

    def createStatistics(self,last):

        from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QVBoxLayout
        from PyQt5.QtCore import Qt

        gLayout = QGridLayout()
        horizontalLayout = QHBoxLayout()
        horizontalLayout.setObjectName("horizontalLayout")
        verticalLayout = QVBoxLayout()
        verticalLayout.setObjectName("verticalLayout")
        verticalLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        verticalLayout.setContentsMargins(10,20,0,0)
        horizontalLayout.addLayout(verticalLayout)
        
        image_package = self.createImage(os.path.join('/usr/share/ubiquity-system-addons','statistics.svg'))
        self.statistics_name_package = self.createName(_(self.translations['statisticsname']))
        self.statistics_description_package = self.createDescription(_(self.translations['statisticsdescription']))
        install_package = self.createCheck('statistics')

        verticalLayout.addWidget(self.statistics_name_package)
        verticalLayout.addWidget(self.statistics_description_package)
        horizontalLayout.addWidget(install_package)

        gLayout.addWidget(image_package,0,0)
        gLayout.addLayout(horizontalLayout,0,1)
        return gLayout

    def createImage(self,path_image):
        from PyQt5.QtWidgets import QLabel, QSizePolicy
        from PyQt5.QtGui import QIcon
        from PyQt5.QtCore import QSize

        label = QLabel()
        label.setText("")
        label.setScaledContents(True)
        label.setPixmap(QIcon(path_image).pixmap(100,100))
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        label.setSizePolicy(sizePolicy)
        label.setMaximumSize(QSize(100,100))
        label.setObjectName("imagePackage")
        return label

    def createName(self,name):
        from PyQt5.QtWidgets import QLabel, QSizePolicy
        from PyQt5.QtGui import QFont

        label_3 = QLabel()
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        label_3.setSizePolicy(sizePolicy)
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        label_3.setFont(font)
        label_3.setObjectName("label_3")
        label_3.setStyleSheet("QLabel{margin-left:5px; }")
        label_3.setText(_(name))
        return label_3

    def createDescription(self,description):
        from PyQt5.QtWidgets import QLabel, QSizePolicy

        label_2 = QLabel()
        label_2.setWordWrap(True)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        label_2.setSizePolicy(sizePolicy)
        label_2.setObjectName("label_2")
        label_2.setStyleSheet("QLabel{margin-left:5px ; color: #666 }")
        label_2.setText(_(description))
        return label_2

    def createCheck(self,action):
        from PyQt5.QtWidgets import QCheckBox, QSizePolicy
        checkBox = QCheckBox()
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        checkBox.setSizePolicy(sizePolicy)
        checkBox.setObjectName("checkBox")
        checkBox.setChecked(self.configuration[action])
        checkBox.clicked.connect(lambda: self.modify_value(action,checkBox))
        return checkBox

    def add_line(self):
        from PyQt5.QtWidgets import QVBoxLayout, QWidget, QSizePolicy

        layout = QVBoxLayout()
        line = QWidget()
        line.setFixedHeight(2)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        line.setSizePolicy(sizePolicy)
        line.setStyleSheet("QWidget{background-color: #ccc}")
        line.setObjectName("line")
        layout.addWidget(line)
        layout.setContentsMargins(20,5,0,0)
        return layout
    
    def modify_value(self, action, checkbox):
        self.configuration[action] = checkbox.isChecked()

class Page(plugin.Plugin):

    @misc.raise_privileges
    def ok_handler(self):
        if not os.path.exists('/var/lib/ubiquity'):
            os.makedirs('/var/lib/ubiquity')
        with open('/var/lib/ubiquity/ubilliurexsystemaddons','w') as fd:
            for x in self.ui.configuration:
                if self.ui.configuration[x]:
                    fd.write(x)
        if self.ui.configuration['flash']:
            with open('/var/lib/ubiquity/lliurex-extra-packages','a') as fd:
                fd.write('adobe-flashplugin\n')
            self.preseed_bool('apt-setup/partner', True)
        else:
            with open('/var/lib/ubiquity/lliurex-extra-packages','r') as fd:
                lines = fd.readlines()
            with open('/var/lib/ubiquity/lliurex-extra-packages','w') as fd:
                for line in lines:
                    if line != 'adobe-flashplugin\n':
                        fd.write(line)

        plugin.Plugin.ok_handler(self)


class Install(plugin.InstallPlugin):
    
    def install(self, target, progress, *args, **kwargs):
        import os
        actions = []
        with open('/var/lib/ubiquity/ubilliurexsystemaddons') as fd:
            actions.append(fd.readline().strip())
        
        if 'flash' in actions:
            if os.path.exists('{}/usr/lib/adobe-flashplugin/libflashplayer.so'.format(target)):
                with open('{}/etc/apt/sources.list.d/canonical.list'.format(target),'w') as fd:
                    fd.write('# AUTOMATICALLY ADDED BY LLIUREX DURING INSTALLATION')
                    fd.write('deb http://archive.canonical.com/ubuntu bionic partner')
                with open('{}/etc/n4d/one-shot/set-flash-configured'.format(target),'w') as fd:
                    fd.write('#!/bin/bash\n')
                    fd.write('zero-center set-configured lliurex-flash-installer')
                os.system('chmod +x {}/etc/n4d/one-shot/set-flash-configured'.format(target))
        
        analytics_path = "{rootmountpoint}/etc/lliurex-analytics/".format(rootmountpoint=target)
        os.system("mkdir -p {ap}".format(ap=analytics_path))
        if 'statistics' in actions:
            with open(os.path.join(analytics_path,"status"),"w") as fd:
                fd.write('yes\n')
        else:
            with open(os.path.join(analytics_path,"status"),"w") as fd:
                fd.write('no\n')

        return plugin.InstallPlugin.install(self, target, progress, *args, **kwargs)
