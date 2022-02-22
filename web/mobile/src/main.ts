import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import "./assets/font_3172792_2ihdsn3t4ny/iconfont.css";
import "./assets/font_3188311_1wipkj1s0u8/iconfont.css"; // 分类图标

import { Tabbar, TabbarItem } from "vant";
import { Icon } from "vant"; // 图标
import { NavBar } from "vant"; // 导航
import { Button } from "vant"; // 图标
import { Cell, CellGroup } from "vant";
import { SwipeCell } from "vant"; // 滑动单元
import { Popover } from "vant";
import { Popup } from "vant";
import { Calendar } from "vant"; // 日历
import { Tag } from "vant"; //标签
import { NoticeBar } from "vant"; // 通知栏
import { ActionSheet } from "vant"; // 动作面板
import { Col, Row } from "vant";
import { Form, Field } from "vant"; // 表单
import { Picker } from "vant"; // 选择器
import { Toast } from "vant"; // 提示
import { Empty } from "vant"; // 空状态
import { List } from "vant"; // 列表, 用于触底事件
import { Step, Steps } from "vant"; // 步骤条
import { Progress } from "vant"; // 进度条
import { Loading } from "vant";
import { Skeleton } from "vant"; // 骨架
import { Switch } from "vant"; // 开关

import Vue3TouchEvents from "vue3-touch-events"; // 滑动事件
// 文档: https://github.com/robinrodricks/vue3-touch-events

const app = createApp(App);

app.use(Tabbar);
app.use(TabbarItem);
app.use(Icon);
app.use(NavBar);
app.use(Button);
app.use(Cell);
app.use(CellGroup);
app.use(SwipeCell);
app.use(Popover);
app.use(Popup);
app.use(Calendar);
app.use(Tag);
app.use(NoticeBar);
app.use(ActionSheet);
app.use(Col);
app.use(Row);
app.use(Form);
app.use(Field);
app.use(Picker);
app.use(Vue3TouchEvents);
app.use(Toast);
app.use(Empty);
app.use(List);
app.use(Loading);
app.use(Step);
app.use(Steps);
app.use(Progress);
app.use(Skeleton);
app.use(Switch);

app.use(store).use(router).mount("#app");
