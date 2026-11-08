# 知枝生活 Skills

10 个面向自然语言需求的综合生活 Skill，适配 `zhizhi-agent-runtime` 本地 Skill Catalog。每个 Skill 独立可用，最终交付均为聊天内 Markdown 文本。

## 能力一览

| Skill | 主要需求 | 特别考虑 |
|---|---|---|
| [food-nutrition](skills/food-nutrition/SKILL.md) | 吃什么、做菜、菜单、备餐、营养与热量估算 | 预算、厨具、过敏、外卖、加班低精力 |
| [fitness](skills/fitness/SKILL.md) | 入门运动、居家训练、力量与有氧、习惯 | 低冲击、剂量与休息、恢复、疼痛停止条件 |
| [healthy-living](skills/healthy-living/SKILL.md) | 睡眠、作息、疲劳、日常习惯 | 倒班与照护约束、少量改变、就医准备 |
| [travel-planner](skills/travel-planner/SKILL.md) | 行程规划与地图查询、准备、预算与取舍 | 老幼同行、首末日、缓冲、备选、待核实项 |
| [personal-finance](skills/personal-finance/SKILL.md) | 工资分配、储蓄、还款、消费、分摊 | 现金缺口、最低偿付、尾差、非羞辱预算 |
| [learning-coach](skills/learning-coach/SKILL.md) | 自学、备考、讲解、练习与复习 | 可检验产物、主动回忆、低门槛重启 |
| [career-assistant](skills/career-assistant/SKILL.md) | 任务排序、沟通汇报、求职与发展 | 容量冲突、真实经历、可复制话术 |
| [home-living](skills/home-living/SKILL.md) | 清洁、收纳、异味、维护与分工 | 恢复功能、材质、化学/燃气/用电风险 |
| [relationship-advisor](skills/relationship-advisor/SKILL.md) | 倾听、沟通、边界、修复与社交 | 尊重自主、不读心、拒绝操控、即时安全 |
| [leisure-entertainment](skills/leisure-entertainment/SKILL.md) | 放松、聚会、兴趣、文字互动 | 可跳过、零准备、不强迫饮酒、不要求产出 |

## 使用与接入

将本项目的 `skills/` 目录部署到 Agent 进程可读位置，并在已有 `api/agent` 配置的 `Skills.Roots` 中添加该目录的**实际绝对路径**。配置授权的只读工具；本次 zhizhi-go 已接入地图发现/调用工具，不启用脚本执行器或业务写入。

开发环境可以配置：

```yaml
Skills:
  Roots:
    - /Volumes/samsungt7/code/aicode/zhizhi/code/zhizhi-skills/skills
  AllowedTools:
    - intelligent_search
    - discover_map_tools
    - call_map_tool
  MaxIterations: 8
  MaxToolCalls: 16
```

若已有其他 Roots，保留原条目后追加，检查名称不能重复。此配置仅为开发机示例，生产环境使用实际部署路径。当前 `api/agent` 在启动时索引目录，更新文件后应按现有发布流程重启/重建 provider；不要假定自动热加载。更完整的执行、上下文传递与权限说明见 [接入设计](docs/design-and-integration.md)。

## 最小验证

在本项目根目录执行（Python 3.9+）：

```sh
python3 tools/validate.py
```

使用相邻 runtime 源码验证真实的加载器与搜索（还需符合该 runtime 要求的 Go 工具链）：

```sh
python3 tools/validate.py --runtime ../zhizhi-agent-runtime
```

该命令仅编译小型开发检查器，临时 Go module 自动清理，不修改 runtime，不运行完整后端测试或构建，不调用模型。首次缺少 Go 依赖缓存时可能由 Go 下载依赖。Skill 的生产执行不依赖 Python 或 Go 检查器；选择使用搜索/地图时需要对应服务可用，失败则退回文本草案。

- [验收案例与实测方法](evals/README.md)：60 条任务案例、10 条路由案例、格式检查和人工标准。
- [参考与取舍](docs/sources.md)：核实过的 GitHub 参考，以及没有引入的依赖。
- [验证记录](docs/verification.md)：实际已验证的部分和仍需模型验收的部分。
- [输出深度评估](docs/output-depth-review.md)：GitHub 原始定义对比、篇幅风险、十个 Skill 的交付粒度，以及宿主二次改写的影响。

计划类请求默认交付可执行方案；单点问答保持直接，完整/多日/多阶段方案按日期和阶段展开。没有统一字数门槛，避免把“内容完整”变成机械长文；用户指定简版、倾诉和游戏互动仍按实际需要回应。

仓库保留原始开发指引；没有自行初始化 Git 仓库、提交或发布。本包完成不等于线上服务已经启用。提示词约束不能替代模型实测或宿主输出验证。
