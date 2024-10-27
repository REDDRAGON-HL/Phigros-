import tkinter as tk
import threading
from tkinter import Toplevel, scrolledtext, END, font
import pandas as pd
from compute import *


def perror():
    window.after(0, lambda: txt.configure(text="参数有误"))
    window.after(0, lambda: par1.delete(0, END))
    window.after(0, lambda: par2.delete(0, END))


def Score():
    """分数计算引导
    a:目标分数，b:物量"""
    
    def thread_task():
        try:
            a = int(par1.get())
            b = int(par2.get())
            if b == 0 or a > 1000000:
                perror()
            else:
                txt.configure(text="目标分数计算\n计算中")
                results = score(b, a)
                window.after(0, lambda: txt.configure(text="目标分数计算,运行结束\n结果请前往运行窗口查看"))
                if checkvar.get() == 1:
                    export(results)
        except Exception:
            perror()
            # 在新线程中运行计算任务
    
    threading.Thread(target=thread_task).start()


def accuracy():
    """acc计算引导
    a:目标acc，b:物量"""
    
    def thread_task():
        try:
            a = float(par1.get())
            b = int(par2.get())
            if b == 0 or a > 100:
                perror()
            else:
                txt.configure(text="目标acc计算\n计算中")
                window.after(0, lambda: txt.configure(text="目标acc计算,运行结束\n我还没写。。"))
        except Exception:
            perror()
    
    threading.Thread(target=thread_task).start()


def ranking():
    """rks计算"""
    try:
        a = float(par1.get())
        b = float(par2.get()) / 100
        if a == 0:
            perror()
        else:
            window.after(0, lambda: txt.configure(
                text=f"单曲rks计算,运行结束\n定数{a},acc{par2.get()}%的单曲rks为{a * b}"))
    except Exception:
        perror()


def export(results):  # 还要做一个GUI上选择导出excel的选项！
    """导出结果"""
    list = []
    for result in results:
        parts = result.split(',')
        dict = {}
        for part in parts:
            key, value = part.split(':')
            if value.isdigit():  # 检查是否为数字，如果是则转换为整数
                dict[key] = int(value)
            else:  # 否则保留为浮点数或字符串（这里acc应该是浮点数）
                try:
                    dict[key] = float(value)
                except ValueError:
                    dict[key] = value
        list.append(dict)
        df = pd.DataFrame(list)
        # 导出为Excel文件
        output_file = 'output.xlsx'
        df.to_excel(output_file, index=False)
    print(f"结果已导出到 {output_file}")


def choose():
    """运行"""
    opta = optvar.get()
    if opta == '目标分数计算':
        Score()
        print()
    elif opta == '目标acc计算':
        accuracy()
    elif opta == '单曲rks计算':
        ranking()


def show(a=None, b=None, c=None):
    """选项显示"""
    def update_text(a=None, b=None, c=None):
        opta = optvar.get()
        if opta == '目标分数计算':
            text.configure(text="参数1输入目标分数，参数2输入物量")
            print("目标分数计算")
        elif opta == '目标acc计算':
            text.configure(text="参数1输入目标acc，参数2输入物量")
            print("目标acc计算")
        elif opta == '单曲rks计算':
            text.configure(text="参数1输入定数，参数2输入acc")
            print("单曲rks计算")
    
    # 监听optvar变化并更新
    optvar.trace("w", update_text)
    # 初始调用以确保文本正确显示
    update_text()


def menuSupport():
    tip = Toplevel(window)
    tip.title("更新与支持")
    tip.geometry('300x200')
    tip.attributes('-alpha', 0.9)
    tip.config(background="#cccccc")
    tip.resizable(0, 0)
    text_area = scrolledtext.ScrolledText(tip, wrap="char", width=40, height=15, background="#cccccc")
    text_area.grid(row=0, column=0, padx=10, pady=10)
    tip.grid_rowconfigure(0, weight=1)
    tip.grid_columnconfigure(0, weight=1)
    placeholders = "<TITLE>"
    style = ("Helvetica", 10, "bold", "blue")
    replacement_titles = ["更新日志", "更新计划", "支持"]
    text = f"""
              {placeholders}
24.10.27 | 优化GUI，增加菜单栏支持选项卡、增加导出结果为Excel表格
24.10.20 | 重写算法，重写GUI

              {placeholders}
算法：编写acc计算、分数计算二分算法、输入蓝键长条数进行更精确计算
计算规则：增加分数区间计算、acc区间计算
GUI：菜单栏切换精准计算和区间计算

                {placeholders}
感谢使用！！！
        
这么屎的代码也要支持吗
若有任何问题或想帮助，欢迎：
Github:REDDRAGON-HL、QQ:798736073叫醒这个废物

        """
    text_area.insert("1.0", text)
    # 设置样式
    font = tk.font.Font(family=style[0], size=style[1], weight=style[2])
    text_area.tag_config("title_tag", font=font, foreground=style[3])
    # 查找替换占位符同时应用样式
    start_index = "1.0"  # 初始搜索位置
    for i, title in enumerate(replacement_titles):  # 查找占位符
        start_index = text_area.search(placeholders, start_index, tk.END)
        if not start_index:  # 如果没有找到退出循环
            break
        end_index = f"{start_index} + {len(placeholders)}c"  # 计算占位符起始结束索引
        # 替换占位符
        centered_title = f" {title} "
        text_area.delete(start_index, end_index)
        text_area.insert(start_index, centered_title + "\n")
        text_area.tag_add("title_tag", start_index, f"{start_index} + {len(centered_title) - 1}c")  # 应用样式
        start_index = f"{end_index} linestart + 1c"  # 更新搜索起始位置到下一行开始


# 创建运行窗口、其他设置
window = tk.Tk()
window.title("Phigros计算")
window.geometry('300x300')
window.config(background="#cccccc")
window.resizable(0, 0)
window.attributes('-alpha', 0.9)

# 菜单栏
menu = tk.Menu(window)
menu.add_command(label="更新与支持", command=menuSupport)

# 提示框及输入框
text = tk.Label(window, text="选择计算方式", bg="#cccccc")
text.place(relx=0, rely=0.035, relwidth=1, relheight=0.1)
par1 = tk.Entry(window)
par1.place(relx=0.1, rely=0.17, relwidth=0.3, relheight=0.1)
par2 = tk.Entry(window)
par2.place(relx=0.6, rely=0.17, relwidth=0.3, relheight=0.1)


# 计算选项控件
optvar = tk.StringVar()
optvar.set("选择计算选项")
opt = tk.OptionMenu(window, optvar, '目标分数计算', '目标acc计算', '单曲rks计算')
opt.place(relx=0.1, rely=0.35, relwidth=0.4, relheight=0.1)
show()

checkvar = tk.IntVar()
check = tk.Checkbutton(window, text="导出结果", variable=checkvar, onvalue=1, offvalue=0, bg="#cccccc")
check.place(relx=0.37, rely=0.58, relwidth=0.26, relheight=0.08)

btn = tk.Button(window, text='运行', command=choose)
btn.place(relx=0.35, rely=0.68, relwidth=0.3, relheight=0.1)

# 输出框
txt = tk.Label(window, text="等待运行", bg="#cccccc")
txt.place(rely=0.83, relwidth=1)

window.config(menu=menu)
window.mainloop()
