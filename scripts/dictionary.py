class MainWindow:
    zh_CN = {
        'Home': '主页',
        'Instances': '实例列表',
        'Basic Task': '基本任务'
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
        'Configuration takes effect after restart': '设置将在应用重启后生效',
        'Maa global settings': 'Maa全局设置',
        'Choose folder': '选择文件夹',
        'Maa default folder': 'Maa默认文件夹'
    }


class AddInstanceMessageBox:
    zh_CN = {
        'Add Instance': '添加实例',
        'Address': '连接地址',
        'Emulator': '模拟器',
        'More': '更多',
        'MuMu Emulator': 'MuMu 模拟器',
        'Name': '名称',
        'Optional, default emulator\'s name': '可选，默认为模拟器名称'
    }


class HomeInterface:
    zh_CN = {
        'MAA Instances': 'MAA实例',
        'Click to switch to the instance management interface': '点击跳转到实例管理界面',
        'Manage application settings, include MAA settings, personalization, etc.': '管理应用设置，包括MAA设置，个性化等',
        'Panel': '仪表盘'
    }


class MaaInstanceInterface:
    zh_CN = {
        'Add': '添加',
        'Edit': '编辑',
        'Current Selection': '当前选择',
        'Instance': '实例',
        'Refresh': '刷新',
        'Card': '卡片',
        'List': '列表',
        'Layout': '布局'
    }


class InstanceDetailMessageBox:
    zh_CN = {
        'Instance Settings': '实例设置'
    }


class TaskInterface:
    zh_CN = {
        'No selected instance': '没有选择实例',
        'Click OK to switch to the instance interface to select one.': '点击确认跳转到实例管理界面选择。',
        'StartUp': '开始唤醒',
        'Fight': '自动作战',
        'Current instance': '当前实例',
        'Recruit': '自动公招',
        'Infrast': '基建排班'
    }


class CoreStatusCard:
    zh_CN = {
        'Maa Core': 'MAA核心',
        'Status': '状态',
        'Checking update': '检查更新中',
        'Reload Maa': '重新加载MAA',
        'Running Instances': '运行中实例',
        'version': '版本',
        'Stop': '停止',
        'Running': '运行中',
        'Updating': '更新中',
        'Loading': '加载中',
        'Warning': '警告'
    }


class LoadingBar:
    zh_CN = {
        'Updating Maa': '正在更新MAA',
        'Loading Maa': '正在加载MAA'
    }


class MaaInstanceCard:
    zh_CN = {
        'No warning': '无警告',
        'Are you sure to remove the instance?': '你确定要移除此实例？',
        'If you remove the instance, it will disappear from the list foverver.\nBut you can backup config/maa.json to '
        'recover data.': '如果你移除了此实例，它将永远消失。\n但你可以备份config/maa.json来恢复数据。',
        'Remove': '移除',
        'Cancel': '取消',
        'Removed': '已移除'
    }


zh_CN = dict(MainWindow.zh_CN.items() |
             SettingInterface.zh_CN.items() |
             AddInstanceMessageBox.zh_CN.items() |
             HomeInterface.zh_CN.items() |
             MaaInstanceInterface.zh_CN.items() |
             InstanceDetailMessageBox.zh_CN.items() |
             TaskInterface.zh_CN.items() |
             CoreStatusCard.zh_CN.items() |
             LoadingBar.zh_CN.items() |
             MaaInstanceCard.zh_CN.items())
