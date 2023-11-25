##coding=utf-8
# 2022-12-21 用 pyecharts 显示柱状图

from pyecharts import options as opts
from pyecharts.charts import Bar


c = (
    Bar()
    .add_xaxis(["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月", ])
    .add_yaxis(
	"数量",
	 [14, 7, 7, 9, 11, 7, 6, 9, 5, 14, 6, 10],
	itemstyle_opts=opts.ItemStyleOpts(color="#789262"),
	)
    .set_global_opts(title_opts=opts.TitleOpts(title="豆瓣年度阅读", subtitle="2022"))
    .render("book.html")
)


