Google IP的国内反向代理
====

在国内建立Google IP的反向代理，防止GFW封锁。
----

问与答

1. 问：如何使用？<br />答：只要简单地在hosts中添加一行代码`121.199.29.119 www.google.com`（如果原来添加过`www.google.com`的IP则需要先删除后再添加），保存后直接访问 https://www.google.com/ 即可。此项目暂时部署在我的阿里云服务器上。
2. 问：很多hosts工具使用后访问Google会403，这个工具能解决吗？<br />答：使用本host，每次会从全球Google IP中随机挑一个，Google不会检测到单个IP连续访问，所以应该不会再出现403。
3. 问：为何只提供https访问访问？你能看到我搜索的内容吗？<br />答：由于SSL的特性，使用https时不管是我还是阿里云还是GFW都无法看到你的搜索内容，也是不提供http访问的原因。
4. 问：为何放在阿里云上？不怕被喝茶吗？<br />答：我们的祖国并不承认封锁了Google，说是Google自己的问题。所以我只是帮Google一下，让大家有个顺畅访问Google的方法，有什么不对呢？

-

说明

1. 我的阿里云的带宽不大，所以鼓励大家可以都来部署到国内的VPS上，分流的同时提供更多的IP。
2. 对性能有点担心，有对Python性能优化有经验的，欢迎fork，欢迎push。
3. 欢迎传播此项目。
4. 部署时也可以修改config.json，指向`accounts.google.com`或`mail.google.com`的443端口，提供访问Gmail的国内IP。
