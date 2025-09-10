import { useEffect, useRef } from 'react'
import BackgroundVideo from './components/BackgroundVideo'
import { useRevealOnScroll } from './hooks/useRevealOnScroll'

type Product = {
  id: number
  title: string
  price: string
  imageUrl: string
}

const sampleProducts: Product[] = Array.from({ length: 9 }).map((_, idx) => ({
  id: idx + 1,
  title: `Product ${idx + 1}`,
  price: `$${(29 + idx * 3).toFixed(2)}`,
  imageUrl: `https://picsum.photos/seed/sp-${idx + 1}/600/400`,
}))

function App() {
  const heroRef = useRef<HTMLDivElement | null>(null)

  useEffect(() => {
    const handleScroll = () => {
      const heroHeight = heroRef.current?.offsetHeight ?? 1
      const progress = Math.min(Math.max(window.scrollY / heroHeight, 0), 1)
      const videoOpacity = 1 - progress
      const overlayOpacity = 1 - progress
      document.documentElement.style.setProperty('--video-opacity', String(videoOpacity))
      document.documentElement.style.setProperty('--hero-overlay-opacity', String(overlayOpacity))
    }
    handleScroll()
    window.addEventListener('scroll', handleScroll, { passive: true })
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  useRevealOnScroll('.reveal')

  return (
    <>
      <BackgroundVideo />

      <section ref={heroRef} className="hero" aria-label="Hero">
        <div>
          <h1>
            Immersive <span className="emph">Dark</span> Shopping
          </h1>
          <p>
            A cinematic landing with a looping video background. Scroll to smoothly transition into products without jarring cuts.
          </p>
          <a className="cta" href="#products">
            Explore products
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden>
              <path d="M12 5v14m0 0l-6-6m6 6l6-6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </a>
        </div>
        <div className="scroll-cue" aria-hidden>
          <svg viewBox="0 0 24 36" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="2.5" y="1.5" width="19" height="33" rx="9.5" stroke="currentColor"/>
            <circle cx="12" cy="9" r="2" fill="currentColor">
              <animate attributeName="cy" values="9;12;9" dur="1.6s" repeatCount="indefinite"/>
            </circle>
          </svg>
          <small>Scroll</small>
        </div>
      </section>

      <section id="products" className="products" aria-label="Products">
        <div className="container">
          <h2 style={{ margin: '0 0 1rem 0' }}>Featured products</h2>
          <p style={{ margin: '0 0 2rem 0', color: 'var(--muted)' }}>
            Hand-picked items just for you.
          </p>
          <div className="grid">
            {sampleProducts.map((p) => (
              <article key={p.id} className="product-card reveal">
                <img className="product-media" src={p.imageUrl} alt="" loading="lazy" />
                <div className="product-content">
                  <h3 className="product-title">{p.title}</h3>
                  <p className="product-price">{p.price}</p>
                </div>
              </article>
            ))}
          </div>
        </div>
      </section>
    </>
  )
}

export default App
