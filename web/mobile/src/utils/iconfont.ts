
/**
 * 阿里iconfont配置 
 **/

// 定义iconfont库
const iconfontVersion = ['1135504_hneleglv0jv']
const iconfontUrlCss = `//at.alicdn.com/t/font_$key.css`
//at.alicdn.com/t/font_8d5l8fzk5b87iudi.css

// 定义动态插入方法
const loadStyle = (url: string) => {
    const link = document.createElement('link')
    link.type = 'text/css'
    link.rel = 'stylesheet'
    link.href = url
    const head = document.getElementsByTagName('head')[0]
    head.appendChild(link)
}

// 动态插入
iconfontVersion.forEach(ele => {
    loadStyle(iconfontUrlCss.replace('$key', ele))
})