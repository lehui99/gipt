Google IP的国内反向代理
====

在国内建立Google IP的反向代理，防止GFW封锁。
----

问与答

1. 问：如何使用？<br />答：只要简单地在hosts中添加一行代码`121.199.29.119 www.google.com`（如果原来添加过`www.google.com`的IP则需要先删除后再添加），保存后直接访问 https://www.google.com/ 即可。此项目暂时部署在我的阿里云服务器上。
2. 问：很多hosts工具使用后访问Google会403，这个工具能解决吗？<br />答：使用本host，每次会从全球Google IP中随机挑一个，Google不会检测到单个IP连续访问，所以应该不会再出现403。
3. 问：为何只提供https访问访问？你能看到我搜索的内容吗？<br />答：由于SSL的特性，使用https时不管是我还是阿里云还是GFW都无法看到你的搜索内容，也是不提供http访问的原因。
4. 问：为何放在阿里云上？不怕被喝茶吗？<br />答：我们的祖国并不承认封锁了Google，说是Google自己的问题。所以我只是帮Google一下，让大家有个顺畅访问Google的方法，有什么不对呢？
5. 问：原理是什么？<br />答：我在阿里云上开了shadowsocks服务，通过shadowsocks服务器做简单的端口转发连接Google服务。特此感谢 https://www.shadowsocks.net/ 提供的免费帐号。

-

说明

1. 我的阿里云的带宽不大，所以鼓励大家可以都来部署到国内的VPS上，分流的同时提供更多的IP。
2. 对性能有点担心，有对Python性能优化有经验的，欢迎fork，欢迎push。
3. 欢迎传播此项目。
4. 部署时也可以修改config.json，指向`accounts.google.com`或`mail.google.com`的443端口，提供访问Gmail的国内IP。

---

如何在国内VPS上部署本项目？
----

1. 运行本项目需要python环境，如果是Windows系统请确保安装了python并且保证python在PATH环境变量中。
2. 项目依赖 https://github.com/Anorov/PySocks ，需要先安装PySocks才能运行（其实不安装也行，直接把socks.py放到和gipt.py同一个目录下即可）。
3. 首先需要准备一至多个shadowsocks帐号，将shadowsocks帐号的配置文件分别保存成ss1config.json、ss2config.json……，和gipt.py放在同一个目录下。
4. TODO:
