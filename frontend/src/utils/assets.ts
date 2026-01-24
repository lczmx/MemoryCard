export const getAssetsFile = (url: string) => {
  return new URL(url, import.meta.url).href
}