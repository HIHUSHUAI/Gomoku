## info

- **timeout_turn** - 每次移动的时间限制（毫秒，0=尽可能快地玩）
- **timeout_match** - 整场比赛的时间限制（毫秒，0=无限制）
- **max_memory** - 内存限制（字节，0=无限制）
- **time_left** - 整场比赛的剩余时间限制（毫秒）
- **game_type** - 0=对手是人类，1=对手是人工智能，2=锦标赛，3=网络锦标赛
- **rule** - 位掩码或总和，1=精确五子连线胜利，2=连续游戏，4=连珠，8=卡罗
- **evaluate** - 表示鼠标光标当前位置的坐标X,Y
- **folder** - 用于持久文件的文件夹

# **必须的命令**

## **START [size]**
当AI接收到此命令时，它会初始化并创建一个空的棋盘，但尚未进行任何移动。参数是棋盘的大小。AI必须能够在20格大小的棋盘上进行游戏，因为这是Gomocup锦标赛中使用的大小。建议但不要求支持其他棋盘大小。如果AI不接受某个大小，它会响应ERROR，并可能在ERROR后跟随一条消息。管理器可以尝试其他大小或向用户显示错误消息。如果AI成功初始化，会响应OK。
示例：
- 管理器发送：
  ```
  START 20
  ```
- AI回答：
  ```
  OK - 一切正常
  ERROR message - 不支持的大小或其他错误
  ```

## **TURN [X],[Y]**
参数是对手移动的坐标。所有坐标从零开始。
预期回答：
两个用逗号分隔的数字——AI的移动坐标。
示例：
- 管理器发送：
  ```
  TURN 10,10
  ```
- AI回答：
  ```
  11,10
  ```

## **BEGIN**
此命令由管理器在比赛开始时发送给其中一个玩家（AI）。这意味着AI预期在空的棋盘上进行开局。之后，另一个AI将接收到包含第一次对手移动的TURN命令。当启用自动开局时，不使用BEGIN命令，因为在那种情况下，两个AI都会接收到BOARD命令。
预期回答：
两个用逗号分隔的数字——AI的移动坐标。
示例：
- 管理器发送：
  ```
  BEGIN
  ```
- AI回答：
  ```
  10,10
  ```

## **BOARD**
此命令完全重设游戏场地。它适合用于已开局比赛的继续或对用户命令进行撤销/重做。BOARD命令通常在棋盘为空时，在START、RESTART或RECTSTART命令之后发送。如果有正在进行的比赛，管理器在发送BOARD命令之前会发送RESTART命令。
之后，形成游戏场地的数据被发送。每一行的格式如下：
```
[X],[Y],[field]
```
其中[X]和[Y]是坐标，[field]是数字1（自己的棋子）、2（对手的棋子）或3（如果启用了连续游戏，棋子是赢得连线的一部分或根据连珠规则是禁手）。
如果游戏规则是连珠，那么管理器必须按照棋子落下的顺序发送这些行。如果游戏规则是五子棋，则管理器可以以任何顺序发送棋步，AI必须能够应对这一点。数据以DONE命令结束。然后，AI预期会像对TURN或BEGIN命令那样作出回答。
示例：
- 管理器发送：
  ```
  BOARD
  10,10,1
  10,11,2
  11,11,1
  9,10,2
  DONE
  ```
- AI回答：
  ```
  9,9
  ```

## **INFO [key] [value]**
管理器向AI发送信息。AI可以忽略这些信息。然而，如果AI超出限制，它将会输掉比赛。AI必须应对管理器没有发送本文档中提到的所有信息的情况。大部分信息在比赛开始时发送。比赛中不会更改时间限制。建议随时响应命令，因为人类对手可以在AI思考时更改这些值。关于时间和内存限制的信息在第

一步移动之前（在START命令之后或之前）发送。info time_left在每次移动前发送（在TURN、BEGIN、BOARD和SWAP2BOARD命令前）。当AI用尽时间时，剩余时间可以是负数。如果整场比赛的时间是无限的，则剩余时间等于2147483647。如果时间有限制，管理器必须发送info time_left信息，以便AI可以忽略info timeout_match，只依赖info time_left。

## **END**
当AI接收到此命令时，必须尽快终止。管理器会等到AI结束。如果终止时间太长（例如1秒），管理器将终止AI。AI在接收到END命令后不应再写入任何输出。然而，管理器不应在AI结束前关闭管道。
预期回答：无
AI应删除其临时文件。

## **ABOUT**
预期AI在一行中发送有关其自身的一些信息。每条信息必须以关键字、等号和引号中的文本值的形式书写。推荐的关键字包括name、version、author、country、www、email。值之间应以逗号分隔，逗号后可以跟空格。管理器可以使用这些信息，但必须能够处理过去只发送人类可读文本的旧AI。
示例：
- 管理器发送：
  ```
  ABOUT
  ```
- AI回答：
  ```
  name="SomeBrain", version="1.0", author="Nymand", country="USA"
  ```

# **可选命令**
此节发布的扩展命令在 Gomocup 锦标赛中不是必须实现的，但对人类玩家特别有用。

## **RECTSTART [宽度],[高度]**
此命令类似于 START 命令，但棋盘是矩形的。参数是两个用逗号分隔的数字。宽度对应 X 坐标，高度属于 Y 坐标。如果棋盘是正方形的，管理器必须使用 START 命令。
示例：
- 管理器发送：
  ```
  RECTSTART 30,20
  ```
- AI 回答：
  ```
  OK - 参数良好
  ERROR message - 不支持矩形棋盘或其他错误
  ```

## **RESTART**
此命令在比赛结束或中止后使用。此命令没有参数。棋盘大小保持不变。AI释放之前的棋盘和其他结构，创建一个新的空棋盘，并为新比赛做准备。然后，AI回答 OK，之后的通信继续如同 START 命令后的通信。如果 AI 回答 UNKNOWN，管理器发送 END 命令并再次执行 AI。
示例：
- 管理器发送：
  ```
  RESTART
  ```
- AI 回答：
  ```
  OK
  ```

## **TAKEBACK [X],[Y]**
此命令用于撤销最后一步移动。AI 移除坐标为 [X,Y] 的棋子，然后回答 OK。
示例：
- 管理器发送：
  ```
  TAKEBACK 9,10
  ```
- AI 回答：
  ```
  OK
  ```

## **PLAY [X],[Y]**
此命令由管理器用来响应 SUGGEST 命令。它强制 AI 执行移动 [X],[Y]。
期望答案：两个用逗号分隔的数字，应与 PLAY 参数相同。如果 AI 不喜欢管理器发送的坐标，它可以回答其他坐标（但不推荐）。
示例：
- AI 发送：
  ```
  SUGGEST 10,10
  ```
- 管理器发送：
  ```
  PLAY 12,10
  ```
- AI 移动到 12,10 并回答：
  ```
  12,10
  ```



## **SWAP2BOARD**

该命令用于处理 Swap2 规则的开局阶段。它在 START 命令和 BOARD 命令之间被发送给 AI 一次或两次。具体有三种情况，每种情况我们都提供了示例：

**案例 1：** 管理器请求前三个棋子。
- 管理器发送：
  ```
  SWAP2BOARD
  DONE
  ```
- AI 回答：
  ```
  7,7 8,7 9,9
  ```

**案例 2：** 管理器发送前三个棋子的坐标，并请求选择选项。
- 管理器发送：
  ```
  SWAP2BOARD
  7,7
  8,7
  9,9
  DONE
  ```
- AI 回答：
  - `SWAP` - 如果 AI 决定交换（选项 1）
  - `8,8` - 如果 AI 决定保持自己的颜色，则输出第四步的坐标（选项 2）
  - `8,8 8,6` - 如果 AI 决定放置两个棋子并让对手选择颜色，则输出第四和第五步的坐标（选项 3）

**案例 3：** 管理器发送前五个棋子的坐标，并请求选择选项。
- 管理器发送：
  ```
  SWAP2BOARD
  7,7
  8,7
  9,9
  8,8
  8,6
  DONE
  ```
- AI 回答：
  - `SWAP` - 如果 AI 决定交换（选项 1）
  - `6,8` - 如果 AI 决定保持自己的颜色，则输出第六步的坐标（选项 2）

在开局阶段之后，棋盘上的棋子将被视为标准比赛的开局。例如，根据案例 3 的上述示例，假设 AI 选择选项 2，管理器将向另一个 AI 发送以下消息：
```
BOARD
7,7,1
8,7,2
9,9,1
8,8,2
8,6,1
6,8,2
DONE
```

作为另一个示例，根据案例 2 的示例，假设 AI 选择选项 1，管理器将向另一个 AI 发送以下消息：
```
BOARD
7,7,2
8,7,1
9,9,2
DONE
```

从您提供的日志内容中，我们可以看到多种调试和信息性消息，特别是以 `DEBUG` 和 `MESSAGE` 开头的行。这些行通常用于输出程序内部状态或执行结果，以便开发者或系统管理员进行问题诊断或性能分析。下面我将详细解释 `MESSAGE` 行及其后面的参数，以及其他相关的 `DEBUG` 信息：

### `MESSAGE` 行解释

```plaintext
MESSAGE depth 19-16 ev -M16 n 18k n/ms 1262 tm 15 pv Oj7 Xf3 Oe2 Xg6 Oi4 Xf6 Oh6 Xe6 Of5 Xd5
```

- **depth 19-16**：表示搜索的深度范围，从 19 层深减少到 16 层。这通常表示搜索算法在不同的层级上进行了操作。
- **ev -M16**：表示评估值（evaluation value）。`-M16` 可能表示一个非常不利的评估结果，`M` 可能代表负无穷大（即胜负已定的局面），这里 `-M16` 代表对方在16步内必胜。
- **n 18k**：表示在搜索过程中评估了大约18000个节点。
- **n/ms 1262**：表示每毫秒处理的节点数，1262个节点/毫秒，反映了搜索的效率。
- **tm 15**：表示用于这次搜索的时间（以毫秒为单位），此处为15毫秒。
- **pv Oj7 Xf3 Oe2 Xg6 Oi4 Xf6 Oh6 Xe6 Of5 Xd5**：代表主要变化线（principal variation），即在当前搜索深度下，预测的最佳棋步序列。`O` 和 `X` 代表不同的玩家，后面的字母和数字组合（如 `j7`、`f3` 等）代表棋盘上的位置。

### `DEBUG` 行解释

`DEBUG` 行提供了各种调试信息，如下所示：

- **Thread j7 O \ 28 -31984 19**：可能指示某个特定线程正在处理与棋盘位置 `j7` 相关的计算。`-31984` 可能是评分，`19` 可能是该位置的某种特定指标。
- **VOTES1** 和 **VOTES2**：可能表示某种形式的投票或优先级评分，用于决定AI的行动。
- **Max S -31984 -31984** 和 **Score -31984 -31984**：显示最大分数和当前分数，可能是AI评估的不同阶段的分数。
- **Board Search, hash**：显示了一个棋盘搜索的哈希值，这可能是为了快速检索相同棋盘配置的搜索结果。
- **Dim 15, 15, Ply 6**：可能指棋盘的维度是15x15，当前深度（Ply）为6。

这些 `DEBUG` 和 `MESSAGE` 行为开发者提供了程序执行时的详细内部状态，有助于优化算法性能或进行错误诊断。


MESSAGE 信息解释
MESSAGE depth 1-2 ev -M4 n 25 n/ms 12 tm 2 pv Xg7
depth 1-2：搜索深度从1到2。
ev -M4：评估值，"-M4" 可能表示一种负面的最大值或紧急状态，通常在棋类游戏中用于表示必输或强势位置。
n 25：在这个深度下考虑的节点数。
n/ms 12：每毫秒处理的节点数。
tm 2：时间（可能是秒或毫秒）。
pv Xg7：最佳走法序列的首步，这里是在 "g7" 位置放置一个 'X'。