// import parseTime, formatTime and set to filter
export { parseTime, formatTime } from '@/utils'

/**
 * Show plural label if time is plural number
 * @param {number} time
 * @param {string} label
 * @return {string}
 */
function pluralize(time, label) {
  if (time === 1) {
    return time + label
  }
  return time + label + 's'
}

/**
 * @param {number} time
 */
export function timeAgo(time) {
  const between = Date.now() / 1000 - Number(time)
  if (between < 3600) {
    return pluralize(~~(between / 60), ' 分钟')
  } else if (between < 86400) {
    return pluralize(~~(between / 3600), ' 小时')
  } else {
    return pluralize(~~(between / 86400), ' 天')
  }
}

/**
 * Number formatting
 * like 10000 => 10k
 * @param {number} num
 * @param {number} digits
 */
export function numberFormatter(num, digits) {
  const si = [
    { value: 1E18, symbol: 'E' },
    { value: 1E15, symbol: 'P' },
    { value: 1E12, symbol: 'T' },
    { value: 1E9, symbol: 'G' },
    { value: 1E6, symbol: 'M' },
    { value: 1E3, symbol: 'k' }
  ]
  for (let i = 0; i < si.length; i++) {
    if (num >= si[i].value) {
      return (num / si[i].value).toFixed(digits).replace(/\.0+$|(\.[0-9]*[1-9])0+$/, '$1') + si[i].symbol
    }
  }
  return num.toString()
}

/**
 * 10000 => "10,000"
 * @param {number} num
 */
export function toThousandFilter(num) {
  return (+num || 0).toString().replace(/^-?\d+/g, m => m.replace(/(?=(?!\b)(\d{3})+$)/g, ','))
}

/**
 * Upper case first char
 * @param {String} string
 */
export function uppercaseFirst(string) {
  return string.charAt(0).toUpperCase() + string.slice(1)
}

/**
 * 在左边用指定内容填充至指定长度
 * @param {*} str 被填充的字符串
 * @param {Number} len 目标长度
 * @param {String} ch 用于填充的内容
 */
export function ljust(str, len, ch) {
  if (typeof str !== 'string') {
    str = String(str)
  }

  while (str.length < len) {
    str = ch + str
  }

  return str
}

/**
 * 时间戳(ms) 格式化 Filter
 * @param {Number} time 时间(ms)
 */
export function timestampFilter(time) {
  if (time === null || time === undefined) return ''
  const date = (typeof time === 'number' || typeof time === 'string') ? new Date(time) : time
  return date.getFullYear() + '年' + ljust(date.getMonth() + 1, 2, '0') + '月' + ljust(date.getDate(), 2, '0') + '日 ' + ljust(date.getHours(), 2, '0') + ':' + ljust(date.getMinutes(), 2, '0') + ':' + ljust(date.getSeconds(), 2, '0')
}
