import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import "./assets/font_3172792_vd2ddqnffc/iconfont.css"

import { Tabbar, TabbarItem } from 'vant';
import { Icon } from 'vant';  // 图标
import { NavBar } from 'vant';  // 导航
import { Button } from 'vant';  // 图标
import { Loading } from 'vant';  // 加载
import { Cell, CellGroup } from 'vant';
import { SwipeCell } from 'vant';  // 滑动单元
import { Popover } from 'vant';
import { Popup } from 'vant';
import { Calendar } from 'vant';  // 日历
import { Tag } from 'vant';  //标签




const app = createApp(App)

app.use(Tabbar);
app.use(TabbarItem);
app.use(Icon);
app.use(NavBar);
app.use(Button);
app.use(Loading);
app.use(Cell);
app.use(CellGroup);
app.use(SwipeCell);
app.use(Popover);
app.use(Popup);
app.use(Calendar);
app.use(Tag);


app.use(store).use(router).mount('#app')
