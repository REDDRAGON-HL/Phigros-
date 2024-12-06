"""
打击获得perfect判定时获得100 % 的分数，
获得good判定时获得65 % 的分数，
获得miss时无分数，

上述判定分数满分为900000，计算方式为：
（perfect数 + good数0.65） / 谱面物量 * 900000（谱面物量是指该谱面获得全连时的连击数）；

另外有100000为连击得分，计算方式为：
最大连击数 / 谱面物量 * 100000；

总分为判定分数 + 连击得分，四舍五入取整。
"""


def rounding(num, n=0):
    """功能: 优化Python内置的round()
    解决Python四舍六入的问题，实现真正的四舍五入。
    参数:
        num: 需要四舍五入的数字:
        n: 保留的小数点位数，默认取整。
    """
    if '.' in str(num):
        if len(str(num).split('.')[1]) > n and str(num).split('.')[1][n] == '5':
            num += 1 * 10 ** -(n + 1)
    if n:
        return round(num, n)
    else:
        return round(num)


def btf(p, g, wl):
    """基础分数"""
    return (p + g * 0.65) / wl * 900000


def cp(ljs, wl):
    """连击分数"""
    return ljs / wl * 100000


# volume物量，target目标，noc情况数量，nocl情况列表，btf基础总分，cp连击分


def fscore1(volume, target):
    """常规算法"""
    noc = 0
    nocl = []
    dicz = {}  # 缓存中间结果
    
    def score1_1(noc, nocl, dicz):
        """常规算法计算部"""
        key = (p, volume, target)
        if key in dicz:
            return noc, nocl
        
        max_g = volume - p  # 最大G
        min_ljs = volume // (max_g + 1) if max_g > 0 else volume  # 最小连击数（全为Miss
        max_ljs = p + max_g  # 最大连击数（全为P或G
        
        for g in range(max_g + 1):
            m = volume - p - g
            btf_score = btf(p, g, volume)
            
            if btf_score > target:  # 如果基础分高于目标
                break
            
            ljs_lower = max(min_ljs, volume // (m + 1) if m > 0 else volume)  # 实际最小连击数
            ljs_upper = min(max_ljs, p + g)  # 实际最大连击数
            
            for ljs in range(ljs_lower, ljs_upper + 1):
                total_score = rounding(btf_score + cp(ljs, volume))
                if total_score == target:
                    noc += 1
                    acc = rounding((p + g * 0.65) / volume, 4)
                    print(f"P:{p},G:{g},M:{m},最大连击:{ljs},acc:{acc}")
                    nocl.append(f"P:{p},G:{g},M:{m},最大连击:{ljs},acc:{acc}")
        dicz[key] = (noc, nocl)
        return noc, nocl
    
    try:
        if target < 500000:
            # 正算
            for p in range(volume + 1):
                noc, nocl = score1_1(noc, nocl, dicz)
        else:
            # 反算
            for i in range(volume + 1):
                p = volume - i
                noc, nocl = score1_1(noc, nocl, dicz)
    
    except KeyboardInterrupt:
        print("\n运行终止，返回现有结果")
    
    print("-" * 50)
    print(f"{noc}种情况")
    print(nocl)
    return nocl


def faccuracy1(volume, acc):
    """常规算法"""
    noc = 0
    nocl = []
    acc00 = acc / 100
    
    def accuracy1_1(noc):
        """常规算法计算部"""
        for g in range(volume - p):
            m = volume - p - g
            now_acc = rounding((p + g * 0.65) / volume, 4)
            if now_acc == acc00:
                noc += 1
                print(f"P:{p},G:{g},M:{m}")
                nocl.append(f"P:{p},G:{g},M:{m}")
        return noc, nocl
    
    try:
        if acc00 < 0.5:
            # 正算
            for p in range(volume + 1):
                noc, nocl = accuracy1_1(noc)
        else:
            # 反算
            for i in range(volume + 1):
                p = volume - i
                noc, nocl = accuracy1_1(noc)
    
    except KeyboardInterrupt:
        print("\n运行终止，返回现有结果")
    
    print("-" * 50)
    print(f"acc {acc}%\n{noc}种情况")
    print(nocl)
    return nocl


def iaccuracy1(volume, acc1, acc2):
    """常规算法"""
    noc = 0
    nocl = []
    acc10 = acc1 / 100
    acc20 = acc2 / 100
    
    def accuracy1_1(noc):
        """常规算法计算部"""
        for g in range(volume - p):
            m = volume - p - g
            now_acc = rounding((p + g * 0.65) / volume, 4)
            show_acc = rounding(now_acc * 100, 4)
            if acc10 <= now_acc <= acc20:
                noc += 1
                print(f"P:{p},G:{g},M:{m},acc:{show_acc}%")
                nocl.append(f"P:{p},G:{g},M:{m},acc:{show_acc}%")
        return noc, nocl
    
    try:
        for i in range(volume + 1):
            p = volume-i
            noc, nocl = accuracy1_1(noc)
    
    except KeyboardInterrupt:
        print("\n运行终止，返回现有结果")
    
    print("-" * 50)
    print(f"{noc}种情况")
    print(nocl)
    return nocl
