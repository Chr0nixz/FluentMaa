class MainWindow:
    zh_CN = {
        'Home': '主页',
        'Instances': '实例列表'
    }


class SettingInterface:
    zh_CN = {
        'Settings': '设置',
        'Personalization': '个性化',
        'Mica effect': '云母效果',
        'Apply semi transparent to windows and surfaces': '窗口和表面显示半透明',
        'Application theme': '应用主题',
        'Change the appearance of your application': '调整你的应用外观',
        'Light': '浅色',
        'Dark': '深色',
        'Use system setting': '跟随系统设置',
        'Language': '语言',
        'Set your preferred language for UI': '选择界面所使用的语言',
        'Theme color': '主题颜色',
        'Change the theme color of you application': '改变应用的主题颜色',
        'Interface zoom': '界面缩放',
        'Change the size of widgets and fonts': '改变组件和字体的大小',
        'Updated successfully': '更新成功',
        'Configuration takes effect after restart': '设置将在应用重启后生效'
    }


class AddInstanceMessageBox:
    zh_CN = {
        'Add Instance': '添加实例',
        'Address': '连接地址',
        'Simulator': '模拟器',
        'More': '更多',
        'MuMu Simulator': 'MuMu 模拟器'
    }


class HomeInterface:
    zh_CN = {
        'MAA Instances': 'MAA实例',
        'Click to switch to the instance management interface': '点击跳转到实例管理界面',
        'Manage application settings, include MAA settings, personalization, etc.': '管理应用设置，包括MAA设置，个性化等',
    }


class MaaInstanceInterface:
    zh_CN = {
        'Add': '添加',
        'Edit': '编辑'
    }


zh_CN = dict(MainWindow.zh_CN.items() |
             SettingInterface.zh_CN.items() |
             AddInstanceMessageBox.zh_CN.items() |
             HomeInterface.zh_CN.items() |
             MaaInstanceInterface.zh_CN.items())
