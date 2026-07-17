import os
import sys
import io
import shutil
import subprocess

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 模板文件所在的目录（所有模板都放在这里）
TEMPLATE_DIR = r"E:\项目\[测试用例模板]+[变更单模板]"
# 复制后生成的项目文件夹根目录
PROJECT_ROOT = r"E:\项目"


def fuzzy_match(keyword, text):
    """模糊匹配：keyword 是否包含在 text 中（不区分大小写）"""
    return keyword.lower() in text.lower()


def listdir_fixed(path):
    """列出目录内容，兼容中文路径编码"""
    try:
        names = os.listdir(path)
        fixed = []
        for n in names:
            try:
                fixed.append(n.encode('gbk').decode('utf-8'))
            except (UnicodeEncodeError, UnicodeDecodeError, AttributeError):
                fixed.append(n)
        return fixed
    except Exception:
        return os.listdir(path)


class ProjectCopyfile:
    """
    根据输入的模板关键词，从模板目录中模糊匹配模板文件，
    然后创建项目文件夹、复制文件、重命名文件。
    """

    def __init__(self, target_folder_name, template_keyword):
        """
        :param target_folder_name: 项目文件夹名（新建的文件夹名称）
        :param template_keyword:   模板名称关键词（模糊匹配 TEMPLATE_DIR 中的文件名）
        """
        self.target_folder_name = target_folder_name
        self.template_keyword = template_keyword
        self.matched_files = []
        self.final_paths = []  # 重命名后的最终文件路径列表，用于后续打开

        # 在模板目录中搜索匹配的文件
        if not os.path.isdir(TEMPLATE_DIR):
            raise FileNotFoundError(f"模板目录不存在: {TEMPLATE_DIR}")

        all_files = []
        for fname in listdir_fixed(TEMPLATE_DIR):
            full = os.path.join(TEMPLATE_DIR, fname)
            if os.path.isfile(full):
                all_files.append(fname)

        if not all_files:
            raise FileNotFoundError(f"模板目录中没有文件: {TEMPLATE_DIR}")

        # 模糊匹配文件名
        for fname in all_files:
            if fuzzy_match(template_keyword, fname):
                self.matched_files.append(fname)

        if not self.matched_files:
            # 列出可用模板供用户参考
            available = "\n".join(f"  · {f}" for f in sorted(all_files))
            raise FileNotFoundError(
                f"在模板目录中找不到包含 '{template_keyword}' 的文件。\n"
                f"可用的模板文件有：\n{available}"
            )

        print(f"关键词 '{template_keyword}' 匹配到 {len(self.matched_files)} 个文件：")
        for f in self.matched_files:
            print(f"  → {f}")

    def get_target_folder_path(self):
        """获取目标项目文件夹的完整路径"""
        return os.path.join(PROJECT_ROOT, self.target_folder_name)

    def copy_files(self):
        """将匹配到的模板文件复制到目标项目文件夹中"""
        target_folder = self.get_target_folder_path()

        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
            print(f"创建文件夹: {target_folder}")

        for file_name in self.matched_files:
            src_path = os.path.join(TEMPLATE_DIR, file_name)
            target_path = os.path.join(target_folder, file_name)

            if os.path.exists(target_path):
                print(f"⚠ 文件已存在，跳过复制: {target_path}")
                continue

            shutil.copy(src_path, target_path)
            print(f"复制完成: {target_path}")

    def rename_files(self):
        """重命名复制后的文件，将模板名替换为项目名"""
        target_folder = self.get_target_folder_path()

        for file_name in self.matched_files:
            origin_path = os.path.join(target_folder, file_name)

            if not os.path.exists(origin_path):
                print(f"⚠ 文件不存在，跳过重命名: {origin_path}")
                continue

            new_file_name = self._build_new_name(file_name)

            if new_file_name == file_name:
                print(f"保持原名: {file_name}")
                self.final_paths.append(origin_path)
                continue

            new_path = os.path.join(target_folder, new_file_name)

            # 防止目标文件已存在
            if os.path.exists(new_path):
                print(f"⚠ 目标文件已存在，跳过重命名: {new_path}")
                self.final_paths.append(new_path)
                continue

            os.rename(origin_path, new_path)
            print(f"重命名: {file_name} → {new_file_name}")
            self.final_paths.append(new_path)

    def _build_new_name(self, file_name):
        """根据模板文件名构建新的项目文件名"""
        name_without_ext, ext = os.path.splitext(file_name)

        # 去掉文件名开头的常见前缀符号
        clean_name = name_without_ext.lstrip('-— 　')

        # 处理包含"用例"的模板文件
        if fuzzy_match("用例", file_name):
            if fuzzy_match("空模板", file_name):
                return self.target_folder_name + '-用例.xlsx'
            elif fuzzy_match("常规模板", file_name):
                return self.target_folder_name + '-用例(常规模板).xlsx'
            elif fuzzy_match("报表模板", file_name):
                return self.target_folder_name + '-用例(报表模板).xlsx'
            elif fuzzy_match("充电模板", file_name):
                return self.target_folder_name + '-用例(充电模板).xlsx'
            elif fuzzy_match("医院模板", file_name):
                return self.target_folder_name + '-用例(医院模板).xlsx'
            elif fuzzy_match("第三方支付", file_name) or fuzzy_match("对接第三方", file_name):
                return self.target_folder_name + '-对接第三方支付测试用例模板.xlsx'
            elif ext == '.md':
                return self.target_folder_name + '-用例.md'
            else:
                # 保留原模板类型标识
                idx = file_name.find('用例')
                return self.target_folder_name + '-' + file_name[idx:]

        # 处理其他类型模板（如"提前缴费模板"等）
        if fuzzy_match("提前缴费", file_name):
            return self.target_folder_name + '-提前缴费模板.xlsx'

        # 兜底：直接加项目名前缀
        if clean_name:
            return self.target_folder_name + '-' + clean_name + ext

        return file_name

    def open_files(self):
        """用系统默认程序打开所有重命名后的文件"""
        for path in self.final_paths:
            if not os.path.exists(path):
                print(f"⚠ 文件不存在，无法打开: {path}")
                continue
            try:
                if sys.platform == 'win32':
                    os.startfile(path)
                elif sys.platform == 'darwin':
                    subprocess.Popen(['open', path])
                else:
                    subprocess.Popen(['xdg-open', path])
                print(f"打开文件: {path}")
            except Exception as e:
                print(f"⚠ 打开文件失败: {path} ({e})")

    def execute(self):
        """执行完整流程：复制文件 → 重命名文件 → 打开文件"""
        self.copy_files()
        self.rename_files()
        print(f"\n✓ 完成！项目文件夹: {self.get_target_folder_path()}")
        self.open_files()


if __name__ == '__main__':
    # ============================================================
    # 方式一：直接修改以下两个参数后运行
    # ============================================================
    PROJECT_NAME = ""          # 项目文件夹名（必填）
    TEMPLATE_KEYWORD = ""      # 模板文件名关键词，模糊匹配（必填）
    # 例如输入 "充电" 会匹配到 "-用例(充电模板).xlsx"
    # 例如输入 "空"   会匹配到 "-用例(空模板).xlsx"
    # 例如输入 "常规" 会匹配到 "-用例(常规模板).xlsx"
    # 例如输入 "提前" 会匹配到 "提前缴费模板.xlsx"

    # ============================================================
    # 方式二：命令行参数
    #   python copyfile.py <项目文件夹名> <模板名称关键词>
    #   示例：python copyfile.py 泉州世界城VIP充电 充电
    #   示例：python copyfile.py 某医院项目 医院
    #   示例：python copyfile.py 某项目 空模板
    # ============================================================

    if len(sys.argv) >= 3:
        project_name = sys.argv[1]
        template_keyword = sys.argv[2]
        ProjectCopyfile(project_name, template_keyword).execute()
    elif PROJECT_NAME and TEMPLATE_KEYWORD:
        ProjectCopyfile(PROJECT_NAME, TEMPLATE_KEYWORD).execute()
    else:
        print("用法：")
        print("  方式一（配置参数）：修改文件中的 PROJECT_NAME 和 TEMPLATE_KEYWORD")
        print("  方式二（命令行参数）：python copyfile.py <项目文件夹名> <模板名称关键词>")
        print()
        print("  模板名称关键词 -- 输入模板文件名中的任意一段即可模糊匹配，例如：")
        print("    充电     → 匹配 -用例(充电模板).xlsx")
        print("    医院     → 匹配 -用例(医院模板).xlsx")
        print("    常规     → 匹配 -用例(常规模板).xlsx")
        print("    报表     → 匹配 -用例(报表模板).xlsx")
        print("    空模板   → 匹配 -用例(空模板).xlsx")
        print("    第三方   → 匹配 -对接第三方支付测试用例模板.xlsx")
        print("    提前     → 匹配 提前缴费模板.xlsx")
        print()
        print("示例：python copyfile.py 泉州世界城VIP充电 充电")
