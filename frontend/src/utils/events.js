export function debounce(delay) {
    let timer;
    return function (callback, ...args) {
        if (timer) clearTimeout(timer)
        timer = setTimeout(() => callback.apply(null, args), delay)
    }
}