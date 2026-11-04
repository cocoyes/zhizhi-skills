# 参考来源与采用边界

查阅日期：2026-11-04。GitHub 内容可能变化，以下为查阅时的方法参考；未复制第三方源码、整段提示词、资源或运行依赖，也未把社区 Skill 当医学、财务权威。不因仓库存在就断言其质量或安全性。

| 来源 | 本次参考点 | 未引入的部分 |
|---|---|---|
| [anthropics/skills](https://github.com/anthropics/skills) | 名称/描述与主体分离，按实际任务组织方法 | 文档文件产物、工具专属要求；格式以知枝本地 runtime 为准 |
| [ZawYePhyo/travel-planner-skill](https://github.com/ZawYePhyo/travel-planner-skill/blob/main/README.md) | 先明确旅行标准、先在聊天内呈现方案 | Wanderlog MCP、研究与预订链路 |
| [SkillMedev nutrition-planner](https://github.com/SkillMedev/skills/blob/main/skills/nutrition-planner/SKILL.md) | 关注可持续性、实际愿意吃的食物、区分临床问题 | 固定热量/蛋白/饮水处方、具体体重干预阈值、多个子 Skill 路由 |
| [recipe-api weekly-meal-planner](https://github.com/recipe-api/claude-skills/blob/main/skills/weekly-meal-planner/SKILL.md) | 区分每份与总量，按人数核算 | 外部食谱/营养 API 和联网验证 |
| [npapatheodorou personal-trainer-skill](https://github.com/npapatheodorou/personal-trainer-skill/blob/main/personal-trainer/SKILL.md) | 注意器械、经验与限制条件 | coach-data 档案、持续写入与跨次追踪 |

## 安全信息核对

- [CDC：使用漂白剂清洁与消毒](https://www.cdc.gov/hygiene/about/cleaning-and-disinfecting-with-bleach.html)：清洁产品不可混用，遵循标签要求。本包没有搬入稀释配方。
- [CDC：氯气化学紧急情况](https://www.cdc.gov/chemical-emergencies/chemical-fact-sheets/chlorine.html)：家庭清洁剂混合可能产生氯气，优先离开暴露区域并寻求适当帮助。本包不提供化学中和教程。
- [NHS：胸痛](https://www.nhs.uk/symptoms/chest-pain/)：胸痛伴头晕、呼吸困难等可能需要紧急救助；本包避免鼓励继续运动，不照搬英国紧急号码用于未知地区。

其他内容为一般生活辅助的原创方法组织，不包装成已验证临床方案；未编造论文、数据、效果保证或最新指南。

未来若直接复用第三方文本、代码或素材，应逐项核实具体文件的许可证与署名要求。当前不替第三方仓库作统一许可声明，也不擅自为本项目指定开源许可证。
