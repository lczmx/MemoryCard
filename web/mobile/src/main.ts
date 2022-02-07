import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import { Tabbar, TabbarItem } from 'vant';
import { Icon } from 'vant';  // 图标
import { NavBar  } from 'vant';  // 导航
import { Button } from 'vant';  // 图标







const app = createApp(App)

app.use(Tabbar);
app.use(TabbarItem);
app.use(Icon);
app.use(NavBar);
app.use(Button);

app.use(store).use(router).mount('#app')
