import time
import typing
import random
import asyncio
from fastapi import BackgroundTasks
from dependencies.orm import get_no_login_user
from service import orm_database
from service.models import Card, Category, User, Plan, Record, Operation
import datetime
from pydantic import BaseModel, EmailStr

# 10sec后复原
await_sec = 5

cards_data = {1: {
    "id": 1,
    "user": 2,
    "category": 1,
    "title": "数据类型",
    "created_at": "2022-03-05 02:07:19",
    "updated_at": "2022-03-05 02:07:19",
    "review_at": "2022-03-05 02:07:19",
    "review_times": 0,
    "summary": r"<p>Redis支持诸如</p><ul><li><p>字符串（strings）</p></li><li><p>哈希（hashes）</p></li><li><p>列表（lists）</p></li><li><p>集合（sets）</p></li><li><p>有序集合（sorted sets ) ( zset）</p></li><li><p>位图（bitmaps）</p></li><li><p>hyperloglogs</p></li><li><p>带半径查询和流的地理空间索引等数据结构（geospatial indexes）。</p></li></ul>",
    "description": r"<ol><li><p>String类型是Redis最基本的数据类型，一个Redis中字符串value最多可以是512M</p><p>String的数据结构为简单动态字符串(Simple Dynamic String,缩写SDS)。是可以修改的字符串</p><ul><li><p><strong>set key value</strong>设置指定 key 的值；NX：key不存在时添加；EX：key超时秒数；PX：key超时毫秒数，与EX互斥</p></li><li><p><strong>get key</strong>获取指定 key 的值</p></li><li><p><strong>append key value</strong>如果 key 已经存在并且是一个字符串， append 命令将指定的 value 追加到该 key 原来值（value）的末尾。</p></li><li><p><strong>strlen key</strong>返回 key 所储存的字符串值的长度。</p></li><li><p><strong>setnx key value</strong>只有在 key 不存在时设置 key 的值。</p></li><li><p><strong>incr key</strong>将 key 中储存的数字值增一。</p></li><li><p><strong>decr key</strong>将 key 中储存的数字值减一</p></li><li><p><strong>getrange key start end</strong>返回 key 中字符串值的子字符</p></li><li><p><strong>getset key value</strong>将给定 key 的值设为 value ，并返回 key 的旧值(old value)。</p></li><li><p><strong>setex key seconds value</strong>将值 value 关联到 key ，并将 key 的过期时间设为 seconds (以秒为单位)。</p></li></ul></li><li><p>Redis 列表是简单的字符串列表，按照插入顺序排序。你可以添加一个元素到列表的头部（左边）或者尾部（右边）。</p><p>首先在列表元素较少的情况下会使用一块连续的内存存储，这个结构是ziplist，也即是压缩列表。它将所有的元素紧挨着一起存储，分配的是一块连续的内存。<br>当数据量比较多的时候才会改成quicklist。因为普通的链表需要的附加指针空间太大，会比较浪费空间。比如这个列表里存的只是int类型的数据，结构上还需要两个额外的指针prev和next。</p><ul><li><p><strong>lpush key value1 [value2]</strong>将一个或多个值插入到列表头部</p></li><li><p><strong>rpush key value1 [value2]</strong>将一个或多个值插入到列表尾部</p></li><li><p><strong>lpop key</strong>移出并获取列表的第一个元素</p></li><li><p><strong>rpop key</strong>移出并获取列表的最后一个元素</p></li><li><p><strong>llen key</strong>获取列表长度</p></li><li><p><strong>rpoplpush source destination</strong>移除source列表的最后一个元素，并将该元素添加到destination列表的头部，并返回</p></li><li><p><strong>lrange key start stop</strong>获取列表指定范围内<code>[start : stop]</code>的元素，可以使用负索引</p></li><li><p><strong>lindex key index</strong>通过索引获取列表中的元素</p></li><li><p><strong>linsert key before/after value1 value2</strong>在value1之前/后插入值value2</p></li><li><p><strong>lrem key count value</strong>从左边删除count个value(从左到右)</p></li><li><p><strong>lset key index value</strong>通过索引设置列表元素的值</p></li></ul></li><li><p>Redis hash 是一个string 类型的field 和value 的映射表。hash特别<strong>适合用于存储对象</strong>。添加，删除操作都是O(1)（平均）。</p><p>Hash类型对应的数据结构是两种：ziplist（压缩列表），hashtable（哈希表）。当field-value长度较短且个数较少时，使用ziplist，否则使用hashtable。</p><ul><li><p><strong>hset key field value</strong>将哈希表 key 中的字段 field 的值设为 value 。</p></li><li><p><strong>hget key field</strong>获取存储在哈希表中指定字段的值。</p></li><li><p><strong>hdel key field1 [field2]</strong>删除一个或多个哈希表字段</p></li><li><p><strong>hexists key field</strong>查看哈希表 key 中，指定的字段是否存在。</p></li><li><p><strong>hkeys key</strong>获取所有哈希表中的字段</p></li><li><p><strong>hvals key</strong>获取哈希表中所有值。</p></li><li><p><strong>hincrby key field increment</strong>为哈希表 key 中的指定字段的整数值加上增量 increment 。</p></li><li><p><strong>hsetnx key field value</strong>只有在字段 field 不存在时，设置哈希表字段的值。</p></li></ul></li><li><p>Redis的Set是string类型的<strong>无序集合</strong>。它<strong>底层其实是一个value为null的hash表</strong>，所以添加，删除，查找的复杂度都是O(1)。</p><p>Set数据结构是dict字典，字典是用哈希表实现的，它的内部使用hash结构，所有的value都指向同一个内部值。</p><ul><li><p><strong>sadd key member1 [member2]</strong>向集合添加一个或多个成员</p></li><li><p><strong>smembers key</strong>返回集合中的所有成员</p></li><li><p><strong>sismember key membe</strong>r判断 member 元素是否是集合 key 的成员</p></li><li><p><strong>scard key</strong>获取集合的成员数<strong>srem </strong></p></li><li><p><strong>key member1 [member2]</strong>移除集合中一个或多个成员</p></li><li><p><strong>spop key</strong>移除并返回集合中的一个随机元素</p></li><li><p><strong>srandmember key [count]</strong>返回集合中一个或多个随机数（不会删除）</p></li><li><p><strong>smove source destination member</strong>将 member 元素从 source 集合移动到 destination 集合</p></li></ul></li><li><p>Redis有序集合zset与普通集合set非常相似，是一个没有重复元素的字符串集合。<br>不同之处是有序集合的每个成员都关联了一个评分（score )</p><p>zset底层使用了两个数据结构:</p><ol><li><p>hash，hash的作用就是关联元素value和权重score，保障元素value的唯一性，可以通过元素value找到相应的score值。</p></li><li><p>跳跃表，跳跃表的目的在于给元素value排序，根据score的范围获取元素列表。</p></li></ol><ul><li><p><strong>zadd key score1 member1 [score2 member2]</strong>向有序集合添加一个或多个成员，或者更新已存在成员的分数</p></li><li><p><strong>zrange key start stop [withscores]</strong>通过索引区间返回有序集合指定区间内的成员，带WITHSCORES，可以让分数一起和值返回到结果集。</p></li><li><p><strong>zrangebyscore key min max [withscores] [limit]</strong>通过分数返回有序集合指定区间内的成员</p></li><li><p><strong>zrevrangebyscore key max min [withscores]</strong>返回有序集中指定分数区间内的成员，分数从高到低排序</p></li><li><p><strong>zincrby key increment member</strong>有序集合中对指定成员的分数加上增量 increment</p></li><li><p><strong>zrem key member [member ...]</strong>移除有序集合中的一个或多个成员</p></li><li><p><strong>zcount key min max</strong>计算在有序集合中指定区间分数的成员数</p></li><li><p><strong>zrank key member</strong>返回有序集合中指定成员的索引，从0开始</p></li></ul></li></ol>",
    "is_star": 0
}, 2: {
    "id": 2,
    "user": 2,
    "category": 1,
    "title": "全局命令",
    "created_at": "2022-03-05 02:11:23",
    "updated_at": "2022-03-05 02:11:23",
    "review_at": "2022-03-05 02:11:23",
    "review_times": 2,
    "summary": r"<p>一般是与key和数据库相关的命令</p>",
    "description": r"<ol><li><p><strong>exists key</strong>检查给定 key 是否存在</p></li><li><p><strong>del key</strong>key 存在时删除 </p></li><li><p>keyrename key newkey修改 key 的名称</p></li><li><p><strong>expire key seconds</strong>为给定 key 设置过期时间，以秒计</p></li><li><p><strong>ttl key</strong>以秒为单位，返回给定 key 的剩余生存时间(ttl, time to live)</p></li><li><p><strong>type key</strong>返回 key 所储存的值的类型</p></li><li><p><strong>select index</strong>选择数据库</p></li><li><p>auth password验证密码</p></li><li><p>dbsize查看当前数据库的key的数量</p></li><li><p>flushdb清空当前库flushall通杀全部库</p></li><li><p>expireat key timestampexpireat 的作用和 expire 类似，都用于为 key 设置过期时间。 不同在于 </p></li></ol>",
    "is_star": 0
}, 3: {
    "id": 3,
    "user": 2,
    "category": 1,
    "title": "发布订阅",
    "created_at": "2022-03-05 02:11:23",
    "updated_at": "2022-03-05 02:11:23",
    "review_at": "2022-03-05 02:11:23",
    "review_times": 0,
    "summary": r"<p>Redis 发布订阅 (pub/sub) 是一种消息通信模式：发送者 (pub) 发送消息，订阅者 (sub) 接收消息。Redis 客户端可以订阅任意数量的频道。</p>",
    "description": r"<p>Redis 发布订阅 (pub/sub) 是一种消息通信模式：发送者 (pub) 发送消息，订阅者 (sub) 接收消息。Redis 客户端可以订阅任意数量的频道。</p><ol><li><p>订阅端</p><p>通过执行命令SUBSCRIBE&nbsp;频道名 [频道名] 监听一个或多个频道，当发布者往频道中发布消息时，客户端就能收到消息。</p></li><li><p>发布端</p><p>打开另一台客户端，往指定频道中发送消息。`publish channel1 message`。</p></li></ol>",
    "is_star": 0
}, 4: {
    "id": 4,
    "user": 2,
    "category": 2,
    "title": "软件包管理",
    "created_at": "2022-03-05 02:11:23",
    "updated_at": "2022-03-05 02:11:23",
    "review_at": "2022-03-05 02:11:23",
    "review_times": 0,
    "summary": r"<p>liunx一般有三种包管理工具</p><ol><li><p>rpm</p></li><li><p>yum</p></li><li><p>apt</p></li></ol>",
    "description": r'<h1 id="rpm">RPM</h1>\n<p>rpm是RedHat Package Manager的缩写，用于互联网打包和安装工具，生成有.rpm扩展名的文件。</p>\n<h2 id="%E6%9F%A5%E8%AF%A2">查询</h2>\n<p><strong>显示已安装</strong><br>\n<code>rpm -qa</code></p>\n<p><strong>查询是否安装</strong><br>\n<code>rpm -qa | grep 包名</code><br>\n或者<code>rpm -q 包名</code><br>\n如：<code>rpm -qa | grep firefox</code>或<code>rpm -q firefox</code><br>\n返回：<code>firefox-60.2.2-1.el7.centos.x86_64</code><br>\n这段文字代表的意思：</p>\n<blockquote>\n<p>firefox: 软件包的名称\n60.2.2-1: 版本号\nel7.centos.x86_64: 使用操作系统</p>\n<blockquote>\n<p>el7是Red Hat 7.x，CentOS 7.x和CloudLinux 7.x的下载。其他的如：el6、el8等以此类推。</p>\n</blockquote>\n</blockquote>\n<blockquote>\n<p>x86_64：64位系统</p>\n<blockquote>\n<p>假如是</p>\n<ol>\n<li>i386/i686表示32位系统(i686是i386的一个子集,仅对应P6及以上级别的CPU，i386则广泛适用于80386以上的各种CPU）</li>\n<li>noarch表示通用</li>\n</ol>\n</blockquote>\n</blockquote>\n<p><strong>查询软件包信息</strong><br>\n<code>rpm -qi 包名</code>，如：<code>rpm -qi firefox</code></p>\n<p><strong>查询软件包的文件</strong><br>\n<code>rpm -ql 包名</code>，如：<code>rpm -ql firefox</code></p>\n<p><strong>查询文件所属软件包</strong><br>\n<code>rpm -qf 路径</code>，如：<code>rpm -qf /etc/passwd</code></p>\n<h2 id="%E5%AE%89%E8%A3%85">安装</h2>\n<p><code>rpm -ivh 软件包的路径</code>(<code>-i</code> 安装; <code>-v</code> 提示;  <code>-h</code> 进度条)</p>\n<h2 id="%E5%8D%B8%E8%BD%BD">卸载</h2>\n<p><code>rpm -e 包名</code><br>\n假如提示有依赖关系的话，建议不要卸载，当然也可以带上<code>--nodeps</code>强制卸载。</p>\n<h1 id="yum">YUM</h1>\n<p>yum是一个基于rpm的shell前端软件管理器，可以从指定服务器中下载rpm包并且安装，不再需要个rpm一样需要提前把包下载到本地，而且yum还能自动处理依赖关系。</p>\n<h2 id="%E6%9F%A5%E8%AF%A2">查询</h2>\n<p><code>yum list | grep 包名</code> 查询服务器是否有需要安装的软件 如：<code>yum list | grep firefox</code>\n<code>yum list installed | grep 包名</code> 查询本地是否已经安装 如：<code>yum list installed | grep firefox</code></p>\n<h2 id="%E5%AE%89%E8%A3%85%E3%80%81%E6%9B%B4%E6%96%B0">安装、更新</h2>\n<p><code>yum install 包名</code> 安装指定yum包, 如：<code>yum install firefox</code><br>\n<code>yum update</code>               全部更新<br>\n<code>yum check-update</code>       检查可更新的程序<br>\n<code>yum update 包名</code>      更新指定软件，如<code>yum updata firefox</code></p>\n<h2 id="%E5%8D%B8%E8%BD%BD">卸载</h2>\n<p><code>yum remove 包名</code> 删除指定的rpm软件包；如：<code>yum remove firefox</code></p>\n<h2 id="%E6%B8%85%E9%99%A4%E7%BC%93%E5%AD%98">清除缓存</h2>\n<p><code>yum clean packages</code>       清除缓存目录下的软件包<br>\n<code>yum clean headers</code>        \t清除缓存目录下的 headers<br>\n<code>yum clean oldheaders</code>   清除缓存目录下旧的 headers</p>\n<h1 id="apt">APT</h1>\n<p>apt是apt advanced packaging tool简称，是Debian Linux发行版中的APT软件包管理工具。所有基于Debian的发行都使用这个包管理系统。deb包可以把一个应用的文件包在一起，大体就如同Windows上的安装文件。</p>\n<h2 id="%E5%AE%89%E8%A3%85">安装</h2>\n<p>注意：通常在安装软件前，通常需要运行<code>sudo apt update</code>获取的最新的软件包列表，以确保您的软件包列表是最新的。\n<code>sudo apt install 包名</code></p>\n<h2 id="%E5%8D%B8%E8%BD%BD">卸载</h2>\n<p><code>sudo apt remove 包名</code></p>\n<h2 id="%E5%85%B6%E4%BB%96">其他</h2>\n<p><code>sudo apt serch 包名</code>  搜索应用程序<br>\n<code>sudo apt show package</code> 获取包信息<br>\n<code>sudo apt source package</code> 下载包的源代码到当前目录<br>\n<code>sudo apt install package --reinstall</code> 重新安装包<br>\n<code>sudo apt upgrade</code> 升级所有可升级的软件包<br>\n<code>sudo apt full-upgrade</code> 在升级软件包时自动处理依赖关系<br>\n<code>sudo apt dist-upgrade</code> 更新包，根据依赖关系的变化，添加包，删除包<br>\n<code>sudo apt purge</code> 删除包,包括配置文件等<br>\n<code>sudo apt build-dep package</code> 安装相关的编译环境，如：<code>sudo apt build-dep apache2</code><br>\n<code>sudo apt autoremove</code>\t自动删除不需要的包<br>\n<code>sudo apt depends package</code> 了解使用该包的依赖包</p>\n<h2 id="%E4%BF%AE%E6%94%B9%E6%BA%90">修改源</h2>\n<p>由于一些linux发行版（如：Ubuntu）的apt源通常是外国的，所以导致安装或更新软件时很慢，通常我们需要修改镜像源地址。\n一些常用的镜像源，<a href="https://www.cnblogs.com/xiaochina/p/5728853.html">点击查看</a></p>\n<p>步骤：</p>\n<ol>\n<li>备份源地址 <code>cp /etc/apt/sources.list /etc/apt/sources.list.bak</code></li>\n<li>修改文件 <code>/etc/apt/sources.list</code></li>\n<li>获取的最新的软件包列表 <code>sudo apt update</code></li>\n</ol>',
    "is_star": 0
}}

category_data = {1: {"id": 1,
                     "user": 2,
                     "plan": 1,
                     "name": "Redis",
                     "icon": "icon-redis",
                     "color": "#ee7959",
                     "is_star": 0
                     }, 2: {
    "id": 2,
    "user": 2,
    "plan": 1,
    "name": "Linux",
    "icon": "icon-linux",
    "color": "#7f9faf",
    "is_star": 0
}}
test_user = {1: {
    "id": 1,
    "username": "nologin",
    "email": "nologin@email.com",
    "hashed_pwd": r"$2b$12$bZLiYlKY6NkC7uUkVjiDqu3CoKsH23E5ldnYgLjrd.f3/K0qT.ASq",
    "phone_number": None,
    "active": 0
}, 2: {
    "id": 2,
    "username": "lczmx",
    "email": "lczmx@foxmail.com",
    "hashed_pwd": r"$2b$12$LrjOqhnRAX2xtyA0QOixsuEfLf8NSOp5144AvwNnswhVpXfox8L2a",
    "phone_number": None,
    "active": 1
}
}

running_tasks = set()  # 防止抖动, 记录正在运行的任务


class RollbackCardModel(BaseModel):
    """
    数据库模型
    """
    id: int
    user: int
    category: int
    title: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    review_at: datetime.datetime
    review_times: int
    summary: str
    description: str
    is_star: int


class RollbackCategoryModel(BaseModel):
    id: int
    user: int
    plan: int
    name: str
    icon: str
    color: str
    is_star: int


class RollbackUserModel(BaseModel):
    id: int
    username: str
    email: EmailStr
    hashed_pwd: str
    phone_number: typing.Optional[str] = None
    active: int


class RollbackRecordModel(BaseModel):
    id: int
    user: typing.Any
    operation: typing.Any
    create_at: datetime.date


def make_background_task(func: typing.Callable):
    """
    将任务放到后台
    """
    func_id = id(func)

    def wrap(background_tasks: BackgroundTasks):
        async def wait_to_thread():
            await asyncio.sleep(await_sec)
            await func()
            if func_id in running_tasks:
                running_tasks.remove(func_id)

        if func_id in running_tasks:
            return
        background_tasks.add_task(wait_to_thread)
        running_tasks.add(func_id)

    return wrap


async def check_database_connect():
    """
    连接数据库
    """
    if not orm_database.is_connected:
        await orm_database.connect()


async def rollback_card(cid: int):
    """
    回滚一张卡片复习
    """
    data = RollbackCardModel(**cards_data.get(cid))
    data.user = await User.objects.filter(pk=data.user).first()
    data.category = await Category.objects.filter(pk=data.category).first()
    # 修改数据
    delay = data.review_at - data.created_at
    time_line = datetime.datetime.now() - datetime.timedelta(hours=12)
    data.created_at = time_line - delay
    data.updated_at = time_line
    data.review_at = time_line
    await reset_data(Card, pk=cid, data=data.dict())


@make_background_task
async def rollback_cards():
    """
    回滚多张卡片复习
    """
    await check_database_connect()
    cards = await Card.objects.all()
    for card in cards:
        if card.pk not in cards_data:
            await card.delete()
    for pk in cards_data:
        await rollback_card(cid=pk)


async def rollback_one_category(cid: int):
    """
    回滚一条类别
    """
    data = RollbackCategoryModel(**category_data.get(cid))
    data.user = await User.objects.filter(pk=data.user).first()
    data.plan = await Plan.objects.filter(pk=data.plan).first()
    await reset_data(Category, pk=cid, data=data.dict())


@make_background_task
async def rollback_all_category():
    """
    回滚多条类别
    """
    await check_database_connect()
    category_lst = await Category.objects.all()

    for category in category_lst:
        if category.pk not in category_data:
            await category.delete()
    for pk in category_data:
        await rollback_one_category(pk)


async def rollback_test_user():
    """
    回滚测试用户
    """
    await check_database_connect()
    users = await User.objects.all()
    for user in users:
        # 判断数据
        if user.pk not in test_user:
            # 多余的user
            await user.delete()

    for pk, data in test_user.items():
        user = await User.objects.filter(pk=pk).first()
        if not user:
            await User.objects.create(**data)
        else:
            await user.update(**data)


@make_background_task
async def rollback_plans():
    """
    回滚复习计划
    删除多余的plan
    """
    await check_database_connect()
    no_login_user = await get_no_login_user()
    plans = await Plan.objects.exclude(user=no_login_user).all()
    for plan in plans:
        await plan.delete()


@make_background_task
async def gen_rand_analyse():
    """
    随机生成操作记录
    """
    random.seed(time.time())
    today = datetime.date.today()
    records = await Record.objects.all()
    already_exists_count = 0
    for record in records:
        already_exists_count += 1
        if record.create_at <= (today - datetime.timedelta(days=200)):
            # 替换已经过期的记录
            # 在7day内有值
            if already_exists_count % 2 == 1:
                date = today - datetime.timedelta(days=random.randint(0, 10))
            else:
                date = today - datetime.timedelta(days=random.randint(0, 200))
            await record.update(create_at=date)

    today_record = await Record.objects.filter(create_at=today).first()
    if today_record:
        return
    # 查看是否需要更新
    user = await User.objects.filter(pk=2).first()
    create_operation = await Operation.objects.filter(pk=2).first()
    review_operation = await Operation.objects.filter(pk=3).first()

    for i in range(already_exists_count + 1, 400 + 1):
        operation = random.choice([create_operation, review_operation])
        date = today - datetime.timedelta(days=random.randint(0, 200))
        data = RollbackRecordModel(id=i, user=user, operation=operation, create_at=date)
        record, created = await Record.objects.get_or_create(pk=i, defaults=data.dict())
        if not created:
            # 已经有数据了, 更新数据
            await record.update(**data.dict())

    # 标记今天已经生成了-- 保底
    data = RollbackRecordModel(id=400, user=user, operation=review_operation, create_at=today)
    record, created = await Record.objects.get_or_create(pk=400, defaults=data.dict())
    if not created:
        # 已经有数据了, 更新数据
        await record.update(**data.dict())


async def reset_data(cls, pk, data):
    """
    重置数据
    """
    instance = await cls.objects.filter(pk=pk).first()
    if instance:
        # 更新数据
        await instance.update(**data)
    else:
        # 创建数据
        await cls.objects.create(**data)
