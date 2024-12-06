import tkinter as tk
import threading
from tkinter import Toplevel, scrolledtext, END, font
import pandas as pd
from compute import *


def perror():
    window.after(0, lambda: txt.configure(text="参数有误"))
    window.after(0, lambda: par1.delete(0, END))
    window.after(0, lambda: par2.delete(0, END))


def fScore():
    """固定分数计算引导
    a:目标分数，b:物量"""
    
    def thread_task():
        try:
            a = int(par1.get())
            b = int(par2.get())
            if b == 0 or a > 1000000:
                perror()
            else:
                txt.configure(text="目标分数计算\n计算中")
                results = fscore1(b, a)
                window.after(0, lambda: txt.configure(text="固定分数计算,运行结束\n结果请前往运行窗口查看"))
                if checkvar.get() == 1:
                    export(results)
        except Exception:
            perror()
            # 在新线程中运行计算任务
    threading.Thread(target=thread_task).start()


def fAccuracy():
    """固定acc计算引导
    a:目标acc，b:物量"""
    
    def thread_task():
        try:
            a = float(par1.get())
            b = int(par2.get())
            if b == 0 or a > 100:
                perror()
            else:
                txt.configure(text="目标acc计算\n计算中")
                results = faccuracy1(b, a)
                window.after(0, lambda: txt.configure(text="固定acc计算,运行结束\n结果请前往运行窗口查看"))
                if checkvar.get() == 1:
                    export(results)
        except Exception:
            perror()
    threading.Thread(target=thread_task).start()


def Ranking():
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


def iScore():
    """区间分数计算引导
    a:目标分数，b:物量"""
    
    def thread_task():
        try:
            window.after(0, lambda: txt.configure(text="施工中"))
        except Exception:
            perror()
            # 在新线程中运行计算任务
    
    threading.Thread(target=thread_task).start()


def iAccuracy():
    """区间acc计算引导
    a1:acc下限，a2:acc上限，b:物量"""
    
    def thread_task():
        try:
            a1 = float(par1.get())
            a2 = float(par2.get())
            b = int(par3.get())
            if b == 0 or a2 > 100 or a1 > a2:
                perror()
            else:
                txt.configure(text="目标acc计算\n计算中")
                results = iaccuracy1(b, a1, a2)
                window.after(0, lambda: txt.configure(text="区间acc计算,运行结束\n结果请前往运行窗口查看"))
                if checkvar.get() == 1:
                    export(results)
        except Exception:
            perror()
    
    threading.Thread(target=thread_task).start()


def export(results):
    window.after(0, lambda: txt.configure(text="运行结束，正在导出"))
    print("运行结束，正在导出")
    """导出结果"""
    list = []
    for result in results:
        parts = result.split(',')
        dict = {}
        for part in parts:
            key, value = part.split(':')
            if value.isdigit():  # 检查是否为数字，如果是则转换为整数
                dict[key] = int(value)
            else:  # 否则保留为浮点数
                try:
                    dict[key] = float(value)
                except ValueError:
                    dict[key] = value
        list.append(dict)
        df = pd.DataFrame(list)
        # 导出为Excel文件
        output = 'output.xlsx'
        df.to_excel(output, index=False)
    window.after(0, lambda: txt.configure(text=f"结果已导出到 {output}"))
    print(f"结果已导出到 {output}")


def choose():
    """运行"""
    opta = optvar.get()
    if opta == '固定分数计算':
        fScore()
        print()
    elif opta == '固定acc计算':
        fAccuracy()
        print()
    elif opta == '单曲rks计算':
        Ranking()
    elif opta == '区间分数计算':
        iScore()
        print()
    elif opta == '区间acc计算':
        iAccuracy()
        print()


def show(a=None, b=None, c=None):
    """选项显示"""
    
    def update_opt(n):
        """更新算法框"""
        opt2['menu'].delete(0, 'end')
        for op in algorithmli[n]:
            opt2['menu'].add_command(label=op, command=lambda x=op: optvar2.set(x))
    
    def update_text(a=None, b=None, c=None):
        """更新提示框"""
        opta = optvar.get()
        if opta == '固定分数计算':
            text.configure(text="参数1输入目标分数，参数2输入物量")
            print("固定分数计算")
            update_opt(0)
        elif opta == '固定acc计算':
            text.configure(text="参数1输入目标acc，参数2输入物量")
            print("固定acc计算")
            update_opt(1)
        elif opta == '单曲rks计算':
            text.configure(text="参数1输入定数，参数2输入acc")
            print("单曲rks计算")
        elif opta == '区间acc计算':
            text.configure(text="参数1输入acc下限，参数2输入acc上限\n参数3输入物量")
            print("区间acc计算")
            update_opt(2)
        elif opta == '区间分数计算':
            text.configure(text="施工中")
            print("区间分数计算")
            update_opt(3)
    
    # 监听optvar变化并更新
    optvar.trace("w", update_text)
    # 初始调用以确保文本正确显示
    update_text()


def menuSupport():
    """菜单栏更新与支持"""
    tip = Toplevel(window)
    tip.title("更新与支持")
    tip.geometry('300x200')
    tip.attributes('-alpha', 0.9)
    tip.config(background="#cccccc")
    tip.resizable(0, 0)
    tip.iconbitmap("favicon.ico")
    text_area = scrolledtext.ScrolledText(tip, wrap="char", width=40, height=15, background="#cccccc")
    text_area.grid(row=0, column=0, padx=10, pady=10)
    tip.grid_rowconfigure(0, weight=1)
    tip.grid_columnconfigure(0, weight=1)
    placeholders = "<TITLE>"
    style = ("Helvetica", 10, "bold", "blue")
    replacement_titles = ["更新日志", "更新计划", "支持"]
    text = f"""
              {placeholders}
24.12.04 | 增加acc计算、区间acc计算
24.11.05 | 添加ico，更新GUI整体框架
24.10.27 | 优化GUI，增加菜单栏支持选项卡、增加导出结果为Excel表格
24.10.20 | 重写算法，重写GUI

              {placeholders}
算法：分数计算二分算法、输入蓝键长条数进行更精确计算
计算规则：分数区间计算
GUI：
其他：编写网页版

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


def fixedCalculations():
    """菜单栏固定计算"""
    opt['menu'].delete(0, 'end')  # 删除所有现有菜单项
    for op in calculationli[0]:
        opt['menu'].add_command(label=op, command=lambda x=op: optvar.set(x))
        optvar.set("选择计算选项")
        par3.place_forget()
        opt.place(relx=0.1, rely=0.35, relwidth=0.4, relheight=0.1)
        opt2.place(relx=0.6, rely=0.35, relwidth=0.3, relheight=0.1)


def intervalCalculation():
    """菜单栏区间计算"""
    opt['menu'].delete(0, 'end')
    for op in calculationli[1]:
        opt['menu'].add_command(label=op, command=lambda x=op: optvar.set(x))
        optvar.set("选择计算选项")
        par3.place(relx=0.1, rely=0.32, relwidth=0.3, relheight=0.1)
        opt.place(relx=0.1, rely=0.46, relwidth=0.4, relheight=0.1)
        opt2.place(relx=0.6, rely=0.46, relwidth=0.3, relheight=0.1)


# 运行窗口和其他设置
window = tk.Tk()
window.title("Phigros计算")
window.geometry('300x300')
window.config(background="#cccccc")
window.resizable(0, 0)
window.attributes('-alpha', 0.9)
window.iconbitmap("favicon.ico")

# 菜单栏和设置
menu = tk.Menu(window)
menu.add_command(label="更新与支持", command=menuSupport)
menu.add_radiobutton(label="固定计算", command=fixedCalculations)
menu.add_radiobutton(label="区间计算", command=intervalCalculation)

# 输入提示及输入框
text = tk.Label(window, text="选择计算方式", bg="#cccccc")
text.place(relx=0, rely=0.035, relwidth=1, relheight=0.1)
par1 = tk.Entry(window)
par1.place(relx=0.1, rely=0.17, relwidth=0.3, relheight=0.1)
par2 = tk.Entry(window)
par2.place(relx=0.6, rely=0.17, relwidth=0.3, relheight=0.1)
par3 = tk.Entry(window)
par3.place()

# 计算选项控件
calculationli = [['固定分数计算', '固定acc计算', '单曲rks计算'], ['区间分数计算', '区间acc计算']]
optvar = tk.StringVar()
optvar.set("选择计算选项")
opt = tk.OptionMenu(window, optvar, '请在菜单栏选择选项')
opt.place(relx=0.1, rely=0.35, relwidth=0.4, relheight=0.1)
show()

algorithmli = [['常规算法', '二分查找'], ['常规算法'], ['常规算法'], ['常规算法']]
optvar2 = tk.StringVar()
optvar2.set("选择算法")
opt2 = tk.OptionMenu(window, optvar2, '请选择计算选项')
opt2.place(relx=0.6, rely=0.35, relwidth=0.3, relheight=0.1)

# 导出、运行、输出提示
checkvar = tk.IntVar()
check = tk.Checkbutton(window, text="导出结果", variable=checkvar, onvalue=1, offvalue=0, bg="#cccccc")
check.place(relx=0.37, rely=0.58, relwidth=0.26, relheight=0.08)
btn = tk.Button(window, text='运行', command=choose)
btn.place(relx=0.35, rely=0.68, relwidth=0.3, relheight=0.1)
txt = tk.Label(window, text="等待运行", bg="#cccccc")
txt.place(rely=0.83, relwidth=1)

window.config(menu=menu)
window.mainloop()
