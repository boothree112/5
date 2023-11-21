# 第二章：数据模型与查询语言
![](img/ch2.png)
> 语言的边界就是思想的边界。
>
> —— 路德维奇・维特根斯坦，《逻辑哲学》（1922）
>

[TOC]

多数应用使用层层叠加的数据模型构建。对于每层数据模型的关键问题是：它是如何用低一层数据模型来 **表示** 的？例如：
2. 当要存储那些数据结构时，你可以利用通用数据模型来表示它们，如 JSON 或 XML 文档、关系数据库中的表或图模型。

一个复杂的应用程序可能会有更多的中间层次，比如基于 API 的 API，不过基本思想仍然是一样的：每个层都通过提供一个明确的数据模型来隐藏更低层次中的复杂性。这些抽象允许不同的人群有效地协作（例如数据库厂商的工程师和使用数据库的应用程序开发人员）。

数据模型种类繁多，每个数据模型都带有如何使用的设想。有些用法很容易，有些则不支持如此；有些操作运行很快，有些则表现很差；有些数据转换非常自然，有些则很麻烦。

## 关系模型与文档模型



多年来，在数据存储和查询方面存在着许多相互竞争的方法。在 20 世纪 70 年代和 80 年代初，网状模型（network model）和层次模型（hierarchical model）曾是主要的选择，但关系模型（relational model）随后占据了主导地位。对象数据库在 20 世纪 80 年代末和 90 年代初来了又去。XML 数据库在二十一世纪初出现，但只有小众采用过。关系模型的每个竞争者都在其时代产生了大量的炒作，但从来没有持续【2】。

随着电脑越来越强大和互联，它们开始用于日益多样化的目的。关系数据库非常成功地被推广到业务数据处理的原始范围之外更为广泛的用例上。你今天在网上看到的大部分内容依旧是由关系数据库来提供支持，无论是在线发布、讨论、社交网络、电子商务、游戏、软件即服务生产力应用程序等内容。


采用 NoSQL 数据库的背后有几个驱动因素，其中包括：

* 需要比关系数据库更好的可伸缩性，包括非常大的数据集或非常高的写入吞吐量
* 相比商业数据库产品，免费和开源软件更受偏爱
* 受挫于关系模型的限制性，渴望一种更具多动态性与表现力的数据模型【5】



目前大多数应用程序开发都使用面向对象的编程语言来开发，这导致了对 SQL 数据模型的普遍批评：如果数据存储在关系表中，那么需要一个笨拙的转换层，处于应用程序代码中的对象和表，行，列的数据库模型之间。模型之间的不连贯有时被称为 **阻抗不匹配（impedance mismatch）**[^i]。

[^i]: 一个从电子学借用的术语。每个电路的输入和输出都有一定的阻抗（交流电阻）。当你将一个电路的输出连接到另一个电路的输入时，如果两个电路的输出和输入阻抗匹配，则连接上的功率传输将被最大化。阻抗不匹配会导致信号反射及其他问题。


![](img/fig2-1.png)
* 传统 SQL 模型（SQL：1999 之前）中，最常见的规范化表示形式是将职位，教育和联系信息放在单独的表中，对 User 表提供外键引用，如 [图 2-1](img/fig2-1.png) 所示。
* 后续的 SQL 标准增加了对结构化数据类型和 XML 数据的支持；这允许将多值数据存储在单行内，并支持在这些文档内查询和索引。这些功能在 Oracle，IBM DB2，MS SQL Server 和 PostgreSQL 中都有不同程度的支持【6,7】。JSON 数据类型也得到多个数据库的支持，包括 IBM DB2，MySQL 和 PostgreSQL 【8】。
* 第三种选择是将职业，教育和联系信息编码为 JSON 或 XML 文档，将其存储在数据库的文本列中，并让应用程序解析其结构和内容。这种配置下，通常不能使用数据库来查询该编码列中的值。
**例 2-1. 用 JSON 文档表示一个 LinkedIn 简介**

```json
{
  "user_id": 251,
  "region_id": "us:91",
  "industry_id": 131,
  "photo_url": "/p/7/000/253/05b/308dd6e.jpg",
    {
      "job_title": "Co-chair",
    },
    }
  "education": [
    {
      "school_name": "Harvard University",
      "start": 1973,
    },
      "end": null
  ],
  "contact_info": {
    "blog": "http://thegatesnotes.com",
  }
```
有一些开发人员认为 JSON 模型减少了应用程序代码和存储层之间的阻抗不匹配。不过，正如我们将在 [第四章](ch4.md) 中看到的那样，JSON 作为数据编码格式也存在问题。缺乏一个模式往往被认为是一个优势；我们将在 “[文档模型中的模式灵活性](#文档模型中的模式灵活性)” 中讨论这个问题。


从用户简介文件到用户职位，教育历史和联系信息，这种一对多关系隐含了数据中的一个树状结构，而 JSON 表示使得这个树状结构变得明确（见 [图 2-2](img/fig2-2.png)）。

![](img/fig2-2.png)

**图 2-2 一对多关系构建了一个树结构**
### 多对一和多对多的关系

在上一节的 [例 2-1]() 中，`region_id` 和 `industry_id` 是以 ID，而不是纯字符串 “Greater Seattle Area” 和 “Philanthropy” 的形式给出的。为什么？

如果用户界面用一个自由文本字段来输入区域和行业，那么将他们存储为纯文本字符串是合理的。另一方式是给出地理区域和行业的标准化的列表，并让用户从下拉列表或自动填充器中进行选择，其优势如下：
* 避免歧义（例如，如果有几个同名的城市）
* 更好的搜索 —— 例如，搜索华盛顿州的慈善家就会匹配这份简介，因为地区列表可以编码记录西雅图在华盛顿这一事实（从 “Greater Seattle Area” 这个字符串中看不出来）

> 数据库管理员和开发人员喜欢争论规范化和非规范化，让我们暂时保留判断吧。在本书的 [第三部分](part-iii.md)，我们将回到这个话题，探讨系统的方法用以处理缓存，非规范化和衍生数据。
不幸的是，对这些数据进行规范化需要多对一的关系（许多人生活在一个特定的地区，许多人在一个特定的行业工作），这与文档模型不太吻合。在关系数据库中，通过 ID 来引用其他表中的行是正常的，因为连接很容易。在文档数据库中，一对多树结构没有必要用连接，对连接的支持通常很弱 [^iii]。


如果数据库本身不支持连接，则必须在应用程序代码中通过对数据库进行多个查询来模拟连接。（在这种情况中，地区和行业的列表可能很小，改动很少，应用程序可以简单地将其保存在内存中。不过，执行连接的工作从数据库被转移到应用程序代码上。）
此外，即便应用程序的最初版本适合无连接的文档模型，随着功能添加到应用程序中，数据会变得更加互联。例如，考虑一下对简历例子进行的一些修改：
* 组织和学校作为实体



  假设你想添加一个新的功能：一个用户可以为另一个用户写一个推荐。在用户的简历上显示推荐，并附上推荐用户的姓名和照片。如果推荐人更新他们的照片，那他们写的任何推荐都需要显示新的照片。因此，推荐应该拥有作者个人简介的引用。
![](img/fig2-3.png)


[图 2-4](img/fig2-4.png) 阐明了这些新功能需要如何使用多对多关系。每个虚线矩形内的数据可以分组成一个文档，但是对单位，学校和其他用户的引用需要表示成引用，并且在查询时需要连接。
![](img/fig2-4.png)


### 文档数据库是否在重蹈覆辙？

在多对多的关系和连接已常规用在关系数据库时，文档数据库和 NoSQL 重启了辩论：如何以最佳方式在数据库中表示多对多关系。那场辩论可比 NoSQL 古老得多，事实上，最早可以追溯到计算机化数据库系统。


IMS 的设计中使用了一个相当简单的数据模型，称为 **层次模型（hierarchical model）**，它与文档数据库使用的 JSON 模型有一些惊人的相似之处【2】。它将所有数据表示为嵌套在记录中的记录树，这很像 [图 2-2](img/fig2-2.png) 的 JSON 结构。
同文档数据库一样，IMS 能良好处理一对多的关系，但是很难应对多对多的关系，并且不支持连接。开发人员必须决定是否复制（非规范化）数据或手动解决从一个记录到另一个记录的引用。这些二十世纪六七十年代的问题与现在开发人员遇到的文档数据库问题非常相似【15】。

那两个模式解决的问题与当前的问题相关，因此值得简要回顾一下那场辩论。


网状模型由一个称为数据系统语言会议（CODASYL）的委员会进行了标准化，并被数个不同的数据库厂商实现；它也被称为 CODASYL 模型【16】。





#### 关系模型



关系数据库的查询优化器是复杂的，已耗费了多年的研究和开发精力【18】。关系模型的一个关键洞察是：只需构建一次查询优化器，随后使用该数据库的所有应用程序都可以从中受益。如果你没有查询优化器的话，那么为特定查询手动编写访问路径比编写通用优化器更容易 —— 不过从长期看通用解决方案更好。

在一个方面，文档数据库还原为层次模型：在其父记录中存储嵌套记录（[图 2-1](img/fig2-1.png) 中的一对多关系，如 `positions`，`education` 和 `contact_info`），而不是在单独的表中。

但是，在表示多对一和多对多的关系时，关系数据库和文档数据库并没有根本的不同：在这两种情况下，相关项目都被一个唯一的标识符引用，这个标识符在关系模型中被称为 **外键**，在文档模型中称为 **文档引用**【9】。该标识符在读取时通过连接或后续查询来解析。迄今为止，文档数据库没有走 CODASYL 的老路。




如果应用程序中的数据具有类似文档的结构（即，一对多关系树，通常一次性加载整个树），那么使用文档模型可能是一个好主意。将类似文档的结构分解成多个表（如 [图 2-1](img/fig2-1.png) 中的 `positions`、`education` 和 `contact_info`）的关系技术可能导致繁琐的模式和不必要的复杂的应用程序代码。

文档模型有一定的局限性：例如，不能直接引用文档中的嵌套的项目，而是需要说 “用户 251 的位置列表中的第二项”（很像层次模型中的访问路径）。但是，只要文件嵌套不太深，这通常不是问题。
文档数据库对连接的糟糕支持可能是个问题，也可能不是问题，这取决于应用程序。例如，如果某分析型应用程序使用一个文档数据库来记录何时何地发生了何事，那么多对多关系可能永远也用不上。【19】。


我们没有办法说哪种数据模型更有助于简化应用代码，因为它取决于数据项之间的关系种类。对高度关联的数据而言，文档模型是极其糟糕的，关系模型是可以接受的，而选用图形模型（请参阅 “[图数据模型](#图数据模型)”）是最自然的。


读时模式类似于编程语言中的动态（运行时）类型检查，而写时模式类似于静态（编译时）类型检查。就像静态和动态类型检查的相对优点具有很大的争议性一样【22】，数据库中模式的强制性是一个具有争议的话题，一般来说没有正确或错误的答案。
在应用程序想要改变其数据格式的情况下，这些方法之间的区别尤其明显。例如，假设你把每个用户的全名存储在一个字段中，而现在想分别存储名字和姓氏【23】。在文档数据库中，只需开始写入具有新字段的新文档，并在应用程序中使用代码来处理读取旧文档的情况。例如：

```go
  // Documents written before Dec 8, 2013 don't have first_name
  user.first_name = user.name.split(" ")[0];

ALTER TABLE users ADD COLUMN first_name text;
UPDATE users SET first_name = substring_index(name, ' ', 1);      -- MySQL

模式变更的速度很慢，而且要求停运。它的这种坏名誉并不是完全应得的：大多数关系数据库系统可在几毫秒内执行 `ALTER TABLE` 语句。MySQL 是一个值得注意的例外，它执行 `ALTER TABLE` 时会复制整个表，这可能意味着在更改一个大型表时会花费几分钟甚至几个小时的停机时间，尽管存在各种工具来解决这个限制【24,25,26】。

大型表上运行 `UPDATE` 语句在任何数据库上都可能会很慢，因为每一行都需要重写。要是不可接受的话，应用程序可以将 `first_name` 设置为默认值 `NULL`，并在读取时再填充，就像使用文档数据库一样。



文档通常以单个连续字符串形式进行存储，编码为 JSON、XML 或其二进制变体（如 MongoDB 的 BSON）。如果应用程序经常需要访问整个文档（例如，将其渲染至网页），那么存储局部性会带来性能优势。如果将数据分割到多个表中（如 [图 2-1](img/fig2-1.png) 所示），则需要进行多次索引查找才能将其全部检索出来，这可能需要更多的磁盘查找并花费更多的时间。

局部性仅仅适用于同时需要文档绝大部分内容的情况。数据库通常需要加载整个文档，即使只访问其中的一小部分，这对于大型文档来说是很浪费的。更新文档时，通常需要整个重写。只有不改变文档大小的修改才可以容易地原地执行。因此，通常建议保持相对小的文档，并避免增加文档大小的写入【9】。这些性能限制大大减少了文档数据库的实用场景。

值得指出的是，为了局部性而分组集合相关数据的想法并不局限于文档模型。例如，Google 的 Spanner 数据库在关系数据模型中提供了同样的局部性属性，允许模式声明一个表的行应该交错（嵌套）在父表内【27】。Oracle 类似地允许使用一个称为 **多表索引集群表（multi-table index cluster tables）** 的类似特性【28】。Bigtable 数据模型（用于 Cassandra 和 HBase）中的 **列族（column-family）** 概念与管理局部性的目的类似【29】。


自 2000 年代中期以来，大多数关系数据库系统（MySQL 除外）都已支持 XML。这包括对 XML 文档进行本地修改的功能，以及在 XML 文档中进行索引和查询的功能。这允许应用程序使用那种与文档数据库应当使用的非常类似的数据模型。

从 9.3 版本开始的 PostgreSQL 【8】，从 5.7 版本开始的 MySQL 以及从版本 10.5 开始的 IBM DB2【30】也对 JSON 文档提供了类似的支持级别。鉴于用在 Web APIs 的 JSON 流行趋势，其他关系数据库很可能会跟随他们的脚步并添加 JSON 支持。
在文档数据库中，RethinkDB 在其查询语言中支持类似关系的连接，一些 MongoDB 驱动程序可以自动解析数据库引用（有效地执行客户端连接，尽管这可能比在数据库中执行的连接慢，需要额外的网络往返，并且优化更少）。


[^v]: Codd 对关系模型【1】的原始描述实际上允许在关系模式中与 JSON 文档非常相似。他称之为 **非简单域（nonsimple domains）**。这个想法是，一行中的值不一定是一个像数字或字符串一样的原始数据类型，也可以是一个嵌套的关系（表），因此可以把一个任意嵌套的树结构作为一个值，这很像 30 年后添加到 SQL 中的 JSON 或 XML 支持。


当引入关系模型时，关系模型包含了一种查询数据的新方法：SQL 是一种 **声明式** 查询语言，而 IMS 和 CODASYL 使用 **命令式** 代码来查询数据库。那是什么意思？

许多常用的编程语言是命令式的。例如，给定一个动物物种的列表，返回列表中的鲨鱼可以这样写：

function getSharks() {
    var sharks = [];
    for (var i = 0; i < animals.length; i++) {
        if (animals[i].family === "Sharks") {
            sharks.push(animals[i]);
        }
    }
```


$$



SELECT * FROM animals WHERE family ='Sharks';


在声明式查询语言（如 SQL 或关系代数）中，你只需指定所需数据的模式 - 结果必须符合哪些条件，以及如何将数据转换（例如，排序，分组和集合） - 但不是如何实现这一目标。数据库系统的查询优化器决定使用哪些索引和哪些连接方法，以及以何种顺序执行查询的各个部分。
声明式查询语言是迷人的，因为它通常比命令式 API 更加简洁和容易。但更重要的是，它还隐藏了数据库引擎的实现细节，这使得数据库系统可以在无需对查询做任何更改的情况下进行性能提升。
SQL 示例不确保任何特定的顺序，因此不在意顺序是否改变。但是如果查询用命令式的代码来写的话，那么数据库就永远不可能确定代码是否依赖于排序。SQL 相当有限的功能性为数据库提供了更多自动优化的空间。



假设你有一个关于海洋动物的网站。用户当前正在查看鲨鱼页面，因此你将当前所选的导航项目 “鲨鱼” 标记为当前选中项目。
            <li>Great White Shark</li>
            <li>Hammerhead Shark</li>
    </li>
            <li>Humpback Whale</li>
            <li>Fin Whale</li>
</ul>
```
现在想让当前所选页面的标题具有一个蓝色的背景，以便在视觉上突出显示。使用 CSS 实现起来非常简单：

```css
li.selected > p {
  background-color: blue;
}

如果使用 XSL 而不是 CSS，你可以做类似的事情：

<xsl:template match="li[@class='selected']/p">
        <xsl:apply-templates/>
```
想象一下，必须使用命令式方法的情况会是如何。在 Javascript 中，使用 **文档对象模型（DOM）** API，其结果可能如下所示：

for (var i = 0; i < liElements.length; i++) {
        var children = liElements[i].childNodes;
            var child = children[j];
            if (child.nodeType === Node.ELEMENT_NODE && child.tagName === "P") {
                child.setAttribute("style", "background-color: blue");
    }
}



在 Web 浏览器中，使用声明式 CSS 样式比使用 JavaScript 命令式地操作样式要好得多。类似地，在数据库中，使用像 SQL 这样的声明式查询语言比使用命令式查询 API 要好得多 [^vi]。
[^vi]: IMS 和 CODASYL 都使用命令式 API。应用程序通常使用 COBOL 代码遍历数据库中的记录，一次一条记录【2,16】。




在 PostgreSQL 中，你可以像这样表述这个查询：

  date_trunc('month', observation_timestamp) AS observation_month,
FROM observations
WHERE family = 'Sharks'
GROUP BY observation_month;
这个查询首先过滤观察记录，以只显示鲨鱼家族的物种，然后根据它们发生的日历月份对观察记录果进行分组，最后将在该月的所有观察记录中看到的动物数目加起来。

同样的查询用 MongoDB 的 MapReduce 功能可以按如下来表述：

```js
        var month = this.observationTimestamp.getMonth() + 1;
        emit(year + "-" + month, this.numAnimals);
    function reduce(key, values) {
    {
        query: {
        out: "monthlySharkReport"

* 可以声明式地指定一个只考虑鲨鱼种类的过滤器（这是 MongoDB 特定的 MapReduce 扩展）。
* 每个匹配查询的文档都会调用一次 JavaScript 函数 `map`，将 `this` 设置为文档对象。
* `map` 函数发出一个键（包括年份和月份的字符串，如 `"2013-12"` 或 `"2014-1"`）和一个值（该观察记录中的动物数量）。
* `map` 发出的键值对按键来分组。对于具有相同键（即，相同的月份和年份）的所有键值对，调用一次 `reduce` 函数。
* 将最终的输出写入到 `monthlySharkReport` 集合中。

  numAnimals: 3
{
  family: "Sharks",
  numAnimals: 4

对每个文档都会调用一次 `map` 函数，结果将是 `emit("1995-12",3)` 和 `emit("1995-12",4)`。随后，以 `reduce("1995-12",[3,4])` 调用 `reduce` 函数，将返回 `7`。
MapReduce 是一个相当底层的编程模型，用于计算机集群上的分布式执行。像 SQL 这样的更高级的查询语言可以用一系列的 MapReduce 操作来实现（见 [第十章](ch10.md)），但是也有很多不使用 MapReduce 的分布式 SQL 实现。请注意，SQL 中没有任何内容限制它在单个机器上运行，而 MapReduce 在分布式查询执行上没有垄断权。

MapReduce 的一个可用性问题是，必须编写两个密切合作的 JavaScript 函数，这通常比编写单个查询更困难。此外，声明式查询语言为查询优化器提供了更多机会来提高查询的性能。基于这些原因，MongoDB 2.2 添加了一种叫做 **聚合管道** 的声明式查询语言的支持【9】。用这种语言表述鲨鱼计数查询如下所示：
```js
db.observations.aggregate([
  { $match: { family: "Sharks" } },
      year:  { $year:  "$observationTimestamp" },
```


## 图数据模型

如我们之前所见，多对多关系是不同数据模型之间具有区别性的重要特征。如果你的应用程序大多数的关系是一对多关系（树状结构化数据），或者大多数记录之间不存在关系，那么使用文档模型是合适的。
但是，要是多对多关系在你的数据中很常见呢？关系模型可以处理多对多关系的简单情况，但是随着数据之间的连接变得更加复杂，将数据建模为图形显得更加自然。

  顶点是人，边指示哪些人彼此认识。
* 网络图谱


可以将那些众所周知的算法运用到这些图上：例如，汽车导航系统搜索道路网络中两点之间的最短路径，PageRank 可以用在网络图上来确定网页的流行程度，从而确定该网页在搜索结果中的排名。



![](img/fig2-5.png)

有几种不同但相关的方法用来构建和查询图表中的数据。在本节中，我们将讨论属性图模型（由 Neo4j，Titan 和 InfiniteGraph 实现）和三元组存储（triple-store）模型（由 Datomic、AllegroGraph 等实现）。我们将查看图的三种声明式查询语言：Cypher，SPARQL 和 Datalog。除此之外，还有像 Gremlin 【36】这样的图形查询语言和像 Pregel 这样的图形处理框架（见 [第十章](ch10.md)）。
### 属性图

* 唯一的标识符
* 一组出边（outgoing edges）
* 一组属性（键值对）

* 唯一标识符
* 边的起点（**尾部顶点**，即 tail vertex）
* 描述两个顶点之间关系类型的标签
* 一组属性（键值对）

**例 2-2 使用关系模式来表示属性图**

```sql
CREATE TABLE vertices (
  vertex_id  INTEGER PRIMARY KEY,
);
CREATE TABLE edges (
  tail_vertex INTEGER REFERENCES vertices (vertex_id),
  label       TEXT,
CREATE INDEX edges_heads ON edges (head_vertex);
```

关于这个模型的一些重要方面是：
1. 任何顶点都可以有一条边连接到任何其他顶点。没有模式限制哪种事物可不可以关联。


你可以想象该图还能延伸出许多关于 Lucy 和 Alain 的事实，或其他人的其他更多的事实。例如，你可以用它来表示食物过敏（为每个过敏源增加一个顶点，并增加人与过敏源之间的一条边来指示一种过敏情况），并链接到过敏源，每个过敏源具有一组顶点用来显示哪些食物含有哪些物质。然后，你可以写一个查询，找出每个人吃什么是安全的。图在可演化性方面是富有优势的：当你向应用程序添加功能时，可以轻松扩展图以适应程序数据结构的变化。

### Cypher 查询语言
**例 2-3 将图 2-5 中的数据子集表示为 Cypher 查询**
CREATE
  (NAmerica:Location {name:'North America', type:'continent'}),
  (Idaho:Location    {name:'Idaho',         type:'state'    }),
当 [图 2-5](img/fig2-5.png) 的所有顶点和边被添加到数据库后，让我们提些有趣的问题：例如，找到所有从美国移民到欧洲的人的名字。更确切地说，这里我们想要找到符合下面条件的所有顶点，并且返回这些顶点的 `name` 属性：该顶点拥有一条连到美国任一位置的 `BORN_IN` 边，和一条连到欧洲的任一位置的 `LIVING_IN` 边。
**例 2-4 查找所有从美国移民到欧洲的人的 Cypher 查询：**
```cypher
  (person) -[:BORN_IN]->  () -[:WITHIN*0..]-> (us:Location {name:'United States'}),
RETURN person.name
```
查询按如下来解读：

> 1.  `person` 顶点拥有一条到某个顶点的 `BORN_IN` 出边。从那个顶点开始，沿着一系列 `WITHIN` 出边最终到达一个类型为 `Location`，`name` 属性为 `United States` 的顶点。
> 2. `person` 顶点还拥有一条 `LIVES_IN` 出边。沿着这条边，可以通过一系列 `WITHIN` 出边最终到达一个类型为 `Location`，`name` 属性为 `Europe` 的顶点。
> 对于这样的 `Person` 顶点，返回其 `name` 属性。

通常对于声明式查询语言来说，在编写查询语句时，不需要指定执行细节：查询优化程序会自动选择预测效率最高的策略，因此你可以专注于编写应用程序的其他部分。


答案是肯定的，但有些困难。在关系数据库中，你通常会事先知道在查询中需要哪些连接。在图查询中，你可能需要在找到待查找的顶点之前，遍历可变数量的边。也就是说，连接的数量事先并不确定。

在我们的例子中，这发生在 Cypher 查询中的 `() -[:WITHIN*0..]-> ()` 规则中。一个人的 `LIVES_IN` 边可以指向任何类型的位置：街道、城市、地区、国家等。一个城市可以在（WITHIN）一个地区内，一个地区可以在（WITHIN）在一个州内，一个州可以在（WITHIN）一个国家内，等等。`LIVES_IN` 边可以直接指向正在查找的位置，或者一个在位置层次结构中隔了数层的位置。

在 Cypher 中，用 `WITHIN*0..` 非常简洁地表述了上述事实：“沿着 `WITHIN` 边，零次或多次”。它很像正则表达式中的 `*` 运算符。


**例 2-5  与示例 2-4 同样的查询，在 SQL 中使用递归公用表表达式表示**
```sql
    UNION
      JOIN in_usa ON edges.head_vertex = in_usa.vertex_id
      WHERE edges.label = 'within'
    in_europe(vertex_id) AS (
    UNION
    SELECT edges.tail_vertex FROM edges
      WHERE edges.label = 'within' ),

  -- born_in_usa 包含了所有类型为 Person，且出生在美国的顶点
    born_in_usa(vertex_id) AS (
        WHERE edges.label = 'born_in' ),

  -- lives_in_europe 包含了所有类型为 Person，且居住在欧洲的顶点。

  FROM vertices
    JOIN born_in_usa ON vertices.vertex_id = born_in_usa.vertex_id
    JOIN lives_in_europe ON vertices.vertex_id = lives_in_europe.vertex_id;
```

* 对于 `in_usa` 集合中的每个顶点，根据 `born_in` 入边来查找出生在美国某个地方的人。
* 同样，对于 `in_europe` 集合中的每个顶点，根据 `lives_in` 入边来查找居住在欧洲的人。

同一个查询，用某一个查询语言可以写成 4 行，而用另一个查询语言需要 29 行，这恰恰说明了不同的数据模型是为不同的应用场景而设计的。选择适合应用程序的数据模型非常重要。

### 三元组存储和 SPARQL
三元组存储模式大体上与属性图模型相同，用不同的词来描述相同的想法。不过仍然值得讨论，因为三元组存储有很多现成的工具和语言，这些工具和语言对于构建应用程序的工具箱可能是宝贵的补充。
在三元组存储中，所有信息都以非常简单的三部分表示形式存储（**主语**，**谓语**，**宾语**）。例如，三元组 **(吉姆, 喜欢, 香蕉)** 中，**吉姆** 是主语，**喜欢** 是谓语（动词），**香蕉** 是对象。
1. 原始数据类型中的值，例如字符串或数字。在这种情况下，三元组的谓语和宾语相当于主语顶点上的属性的键和值。例如，`(lucy, age, 33)` 就像属性 `{“age”：33}` 的顶点 lucy。
2. 图中的另一个顶点。在这种情况下，谓语是图中的一条边，主语是其尾部顶点，而宾语是其头部顶点。例如，在 `(lucy, marriedTo, alain)` 中主语和宾语 `lucy` 和 `alain` 都是顶点，并且谓语 `marriedTo` 是连接他们的边的标签。
[例 2-6]() 展示了与 [例 2-3]() 相同的数据，以称为 Turtle 的格式（Notation3（N3）【39】的一个子集）写成三元组。
```reStructuredText
_:lucy     a       :Person.
_:lucy     :name   "Lucy".
_:lucy     :bornIn _:idaho.
_:idaho    a       :Location.
_:idaho    :type   "state".
_:idaho    :within _:usa.
_:usa      a       :Location
_:usa      :name   "United States"
_:usa      :within _:namerica.
_:namerica :type   :"continent"
```

在这个例子中，图的顶点被写为：`_：someName`。这个名字并不意味着这个文件以外的任何东西。它的存在只是帮助我们明确哪些三元组引用了同一顶点。当谓语表示边时，该宾语是一个顶点，如 `_:idaho :within _:usa.`。当谓语是一个属性时，该宾语是一个字符串，如 `_:usa :name"United States"`


_:idaho     a :Location; :name "Idaho";         :type "state";   :within _:usa
_:usa       a :Loaction; :name "United States"; :type "country"; :within _:namerica.
_:namerica  a :Location; :name "North America"; :type "continent".


如果你深入了解关于三元组存储的信息，可能会陷入关于**语义网**的讨论漩涡中。三元组存储模型其实是完全独立于语义网存在的，例如，Datomic【40】作为一种三元组存储数据库 [^vii]，从未被用于语义网中。但是，由于在很多人眼中这两者紧密相连，我们应该简要地讨论一下。

从本质上讲，语义网是一个简单且合理的想法：网站已经将信息发布为文字和图片供人类阅读，为什么不将信息作为机器可读的数据也发布给计算机呢？（基于三元组模型的）**资源描述框架**（**RDF**）【41】，被用作不同网站以统一的格式发布数据的一种机制，允许来自不同网站的数据自动合并成 **一个数据网络** —— 成为一种互联网范围内的 “通用语义网数据库”。
不幸的是，语义网在二十一世纪初被过度炒作，但到目前为止没有任何迹象表明已在实践中应用，这使得许多人嗤之以鼻。它还饱受眼花缭乱的缩略词、过于复杂的标准提案和狂妄自大的困扰。

然而，如果从过去的失败中汲取教训，语义网项目还是拥有很多优秀的成果。即使你没有兴趣在语义网上发布 RDF 数据，三元组这种模型也是一种好的应用程序内部数据模型。
[例 2-7]() 中使用的 Turtle 语言是一种用于 RDF 数据的人类可读格式。有时候，RDF 也可以以 XML 格式编写，不过完成同样的事情会相对啰嗦，请参阅 [例 2-8]()。Turtle/N3 是更可取的，因为它更容易阅读，像 Apache Jena 【42】这样的工具可以根据需要在不同的 RDF 格式之间进行自动转换。

```xml
        <type>state</type>
        <within>
                <name>United States</name>
                        <name>North America</name>
                </within>
        </within>
    <Person rdf:nodeID="lucy">
        <name>Lucy</name>
    </Person>

RDF 有一些奇怪之处，因为它是为了在互联网上交换数据而设计的。三元组的主语，谓语和宾语通常是 URI。例如，谓语可能是一个 URI，如 `<http://my-company.com/namespace#within>` 或 `<http://my-company.com/namespace#lives_in>`，而不仅仅是 `WITHIN` 或 `LIVES_IN`。这个设计背后的原因为了让你能够把你的数据和其他人的数据结合起来，如果他们赋予单词 `within` 或者 `lives_in` 不同的含义，两者也不会冲突，因为它们的谓语实际上是 `<http://other.org/foo#within>` 和 `<http://other.org/foo#lives_in>`。

从 RDF 的角度来看，URL `<http://my-company.com/namespace>` 不一定需要能解析成什么东西，它只是一个命名空间。为避免与 `http://URL` 混淆，本节中的示例使用不可解析的 URI，如 `urn：example：within`。幸运的是，你只需在文件顶部对这个前缀做一次声明，后续就不用再管了。

### SPARQL 查询语言
```sparql
SELECT ?personName WHERE {
  ?person :livesIn / :within* / :name "Europe".
```

结构非常相似。以下两个表达式是等价的（SPARQL 中的变量以问号开头）：

```
(person) -[:BORN_IN]-> () -[:WITHIN*0..]-> (location)   # Cypher
```


```
(usa {name:'United States'})   # Cypher
?usa :name "United States".    # SPARQL

SPARQL 是一种很好的查询语言 —— 尽管它构想的语义网从未实现，但它仍然是一种可用于应用程序内部的强大工具。

>
> 在 “[文档数据库是否在重蹈覆辙？](#文档数据库是否在重蹈覆辙？)” 中，我们讨论了 CODASYL 和关系模型如何竞相解决 IMS 中的多对多关系问题。乍一看，CODASYL 的网状模型看起来与图模型相似。CODASYL 是否是图形数据库的第二个变种？
> 不，他们在几个重要方面有所不同：
>
> * 在 CODASYL 中，数据库有一个模式，用于指定哪种记录类型可以嵌套在其他记录类型中。在图形数据库中，不存在这样的限制：任何顶点都可以具有到其他任何顶点的边。这为应用程序适应不断变化的需求提供了更大的灵活性。
> * 在 CODASYL 中，达到特定记录的唯一方法是遍历其中的一个访问路径。在图形数据库中，可以通过其唯一 ID 直接引用任何顶点，也可以使用索引来查找具有特定值的顶点。
> * 在 CODASYL 中，所有查询都是命令式的，难以编写，并且很容易因架构变化而受到破坏。在图形数据库中，你可以在命令式代码中手写遍历过程，但大多数图形数据库都支持高级声明式查询，如 Cypher 或 SPARQL。

### 基础：Datalog

[^viii]: Datomic 和 Cascalog 使用 Datalog 的 Clojure S 表达式语法。在下面的例子中使用了一个更容易阅读的 Prolog 语法，但两者没有任何功能差异。

Datalog 的数据模型类似于三元组模式，但进行了一点泛化。把三元组写成 **谓语**（**主语，宾语**），而不是写三元语（**主语，谓语，宾语**）。[例 2-10]() 显示了如何用 Datalog 写入我们的例子中的数据。

```prolog
name(namerica, 'North America').

name(usa, 'United States').
within(usa, namerica).

name(idaho, 'Idaho').
type(idaho, state).

name(lucy, 'Lucy').
```
既然已经定义了数据，我们可以像之前一样编写相同的查询，如 [例 2-11]() 所示。它看起来与 Cypher 或 SPARQL 的语法差异较大，但请不要抗拒它。Datalog 是 Prolog 的一个子集，如果你是计算机科学专业的学生，可能已经见过 Prolog。
**例 2-11 与示例 2-4 相同的查询，用 Datalog 表示**

```
within_recursive(Location, Name) :- within(Location, Via), /* Rule 2 */
                                    born_in(Person, BornLoc),
                                    lives_in(Person, LivingLoc),
                                    within_recursive(LivingLoc, LivingIn).

```
Cypher 和 SPARQL 使用 SELECT 立即跳转，但是 Datalog 一次只进行一小步。我们定义 **规则**，以将新谓语告诉数据库：在这里，我们定义了两个新的谓语，`within_recursive` 和 `migrated`。这些谓语不是存储在数据库中的三元组中，而是从数据或其他规则派生而来的。规则可以引用其他规则，就像函数可以调用其他函数或者递归地调用自己一样。像这样，复杂的查询可以借由小的砖瓦构建起来。
在规则中，以大写字母开头的单词是变量，谓语则用 Cypher 和 SPARQL 的方式一样来匹配。例如，`name(Location, Name)` 通过变量绑定 `Location = namerica` 和 `Name ='North America'` 可以匹配三元组 `name(namerica, 'North America')`。

要是系统可以在 `:-` 操作符的右侧找到与所有谓语的一个匹配，就运用该规则。当规则运用时，就好像通过 `:-` 的左侧将其添加到数据库（将变量替换成它们匹配的值）。
因此，一种可能的应用规则的方式是：
1. 数据库存在 `name (namerica, 'North America')`，故运用规则 1。它生成 `within_recursive (namerica, 'North America')`。



相对于本章讨论的其他查询语言，我们需要采取不同的思维方式来思考 Datalog 方法，但这是一种非常强大的方法，因为规则可以在不同的查询中进行组合和重用。虽然对于简单的一次性查询，显得不太方便，但是它可以更好地处理数据很复杂的情况。

## 本章小结
数据模型是一个巨大的课题，在本章中，我们快速浏览了各种不同的模型。我们没有足够的篇幅来详述每个模型的细节，但是希望这个概述足以激起你的兴趣，以更多地了解最适合你的应用需求的模型。



每个数据模型都具有各自的查询语言或框架，我们讨论了几个例子：SQL，MapReduce，MongoDB 的聚合管道，Cypher，SPARQL 和 Datalog。我们也谈到了 CSS 和 XSL/XPath，它们不是数据库查询语言，而包含有趣的相似之处。



## 参考文献

1.  Michael Stonebraker and Joseph M. Hellerstein: “[What Goes Around Comes Around](http://mitpress2.mit.edu/books/chapters/0262693143chapm1.pdf),” in *Readings in Database Systems*, 4th edition, MIT Press, pages 2–41, 2005. ISBN: 978-0-262-69314-1
1.  Pramod J. Sadalage and Martin Fowler: *NoSQL Distilled*. Addison-Wesley, August 2012. ISBN: 978-0-321-82662-6
1.  Eric Evans: “[NoSQL: What's in a Name?](http://blog.sym-link.com/2009/10/30/nosql_whats_in_a_name.html),” *blog.sym-link.com*, October 30, 2009.
1.  Michael Wagner:  *SQL/XML:2006 – Evaluierung der Standardkonformität ausgewählter Datenbanksysteme*.  Diplomica Verlag, Hamburg, 2010. ISBN: 978-3-836-64609-3
1.  “[XML   Data in SQL Server](http://technet.microsoft.com/en-us/library/bb522446.aspx),” SQL Server 2012 documentation, *technet.microsoft.com*, 2013.
1.  Lin Qiao, Kapil Surlaker, Shirshanka Das, et al.: “[On Brewing Fresh Espresso: LinkedIn’s Distributed Data Serving Platform](http://www.slideshare.net/amywtang/espresso-20952131),” at *ACM International Conference on Management of Data* (SIGMOD), June 2013.
1.  Rick Long, Mark Harrington, Robert Hain, and Geoff Nicholls: <a href="http://www.redbooks.ibm.com/redbooks/pdfs/sg245352.pdf">*IMS Primer*</a>. IBM Redbook SG24-5352-00, IBM International Technical Support Organization, January 2000.
1.  Stephen D. Bartlett: “[IBM’s IMS—Myths, Realities, and Opportunities](ftp://public.dhe.ibm.com/software/data/ims/pdf/TCG2013015LI.pdf),” The Clipper Group Navigator, TCG2013015LI, July 2013.
1.  Sarah Mei: “[Why You Should Never Use MongoDB](http://www.sarahmei.com/blog/2013/11/11/why-you-should-never-use-mongodb/),” *sarahmei.com*, November 11, 2013.
1.  J. S. Knowles and D. M. R. Bell: “The CODASYL Model,” in *Databases—Role and Structure: An Advanced Course*, edited by P. M. Stocker, P. M. D. Gray, and M. P. Atkinson, pages 19–56, Cambridge University Press, 1984. ISBN: 978-0-521-25430-4
1.  Charles W. Bachman: “[The Programmer as Navigator](http://dl.acm.org/citation.cfm?id=362534),” *Communications of the ACM*, volume 16, number 11, pages 653–658, November 1973. [doi:10.1145/355611.362534](http://dx.doi.org/10.1145/355611.362534)
1.  Joseph M. Hellerstein, Michael Stonebraker, and James Hamilton: “[Architecture of a Database System](http://db.cs.berkeley.edu/papers/fntdb07-architecture.pdf),” *Foundations and Trends in Databases*, volume 1, number 2, pages 141–259, November 2007. [doi:10.1561/1900000002](http://dx.doi.org/10.1561/1900000002)
1.  Martin Fowler: “[Schemaless Data Structures](http://martinfowler.com/articles/schemaless/),” *martinfowler.com*, January 7, 2013.
1.  “[Percona Toolkit Documentation: pt-online-schema-change](http://www.percona.com/doc/percona-toolkit/2.2/pt-online-schema-change.html),” Percona Ireland Ltd., 2013.
1.  Rany Keddo, Tobias Bielohlawek, and Tobias Schmidt: “[Large Hadron Migrator](https://github.com/soundcloud/lhm),” SoundCloud, 2013.
1.  Bobbie J. Cochrane and Kathy A. McKnight: “[DB2 JSON Capabilities, Part 1: Introduction to DB2 JSON](http://www.ibm.com/developerworks/data/library/techarticle/dm-1306nosqlforjson1/),” IBM developerWorks, June 20, 2013.
1.  “[The Neo4j Manual v2.0.0](http://docs.neo4j.org/chunked/2.0.0/index.html),” Neo Technology, 2013.
1.  W3C RDF Working Group: “[Resource Description Framework (RDF)](http://www.w3.org/RDF/),” *w3.org*, 10 February 2004.
1.  Steve Harris, Andy Seaborne, and Eric Prud'hommeaux: “[SPARQL 1.1 Query Language](http://www.w3.org/TR/sparql11-query/),” W3C Recommendation, March 2013.
1.  Stefano Ceri, Georg Gottlob, and Letizia Tanca: “[What You Always Wanted to Know About Datalog (And Never Dared to Ask)](https://www.researchgate.net/profile/Letizia_Tanca/publication/3296132_What_you_always_wanted_to_know_about_Datalog_and_never_dared_to_ask/links/0fcfd50ca2d20473ca000000.pdf),” *IEEE Transactions on Knowledge and Data Engineering*, volume 1, number 1, pages 146–166, March 1989. [doi:10.1109/69.43410](http://dx.doi.org/10.1109/69.43410)
1.  Serge Abiteboul, Richard Hull, and Victor Vianu: <a href="http://webdam.inria.fr/Alice/">*Foundations of Databases*</a>. Addison-Wesley, 1995. ISBN: 978-0-201-53771-0, available online at *webdam.inria.fr/Alice*
1.  Nathan Marz: “[Cascalog](http://cascalog.org/),” *cascalog.org*.
1.  Dennis A. Benson,  Ilene Karsch-Mizrachi, David J. Lipman, et al.: “[GenBank](http://nar.oxfordjournals.org/content/36/suppl_1/D25.full-text-lowres.pdf),”   *Nucleic Acids Research*, volume 36, Database issue, pages D25–D30, December 2007.   [doi:10.1093/nar/gkm929](http://dx.doi.org/10.1093/nar/gkm929)


| 上一章                                       | 目录                            | 下一章                       |*$py.class
# Torch Models
*.pkl
current_train.py
video_test*.py
*.swp
# C extensions
.Python
local_test.py
.DS_STORE
.idea/
.vscode/
env/
build/
dist/
.eggs/
lib/
lib64/
parts/
sdist/
*.egg-info/
*.egg

#  Usually these files are written by a python script from a template

pip-log.txt
pip-delete-this-directory.txt
.tox/
.coverage
.cache
nosetests.xml
coverage.xml

*.mo
# Django stuff:
*.log
instance/

.scrapy

# Sphinx documentation
docs/_build/
# PyBuilder

# IPython Notebook
.ipynb_checkpoints
# pyenv


# dotenv
.env

ENV/
# Spyder project settings
# Rope project settings