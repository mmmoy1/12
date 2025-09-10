import { useEffect } from 'react'

export function useRevealOnScroll(selector: string = '.reveal', rootMargin: string = '0px 0px -10% 0px') {
  useEffect(() => {
    const elements = Array.from(document.querySelectorAll<HTMLElement>(selector))
    if (elements.length === 0) return

    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            entry.target.classList.add('in')
            observer.unobserve(entry.target)
          }
        }
      },
      { root: null, rootMargin, threshold: 0.1 }
    )

    elements.forEach((el, idx) => {
      el.style.transitionDelay = `${Math.min(idx * 60, 360)}ms`
      observer.observe(el)
    })

    return () => observer.disconnect()
  }, [selector, rootMargin])
}

