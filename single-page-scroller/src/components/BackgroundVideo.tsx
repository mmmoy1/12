import { useEffect, useRef, useState } from 'react'

export default function BackgroundVideo() {
  const videoRef = useRef<HTMLVideoElement | null>(null)
  const [src, setSrc] = useState<string>('background-video.mp4.mov')

  useEffect(() => {
    let isMounted = true
    const prefer = async (path: string) => {
      try {
        // Use relative fetch so it works under GitHub Pages base path
        const res = await fetch(path, { method: 'HEAD' })
        if (!isMounted) return
        if (res.ok) setSrc(path)
      } catch {
        // ignore
      }
    }
    // Priority order: Firebase file -> custom GitHub file -> default background
    prefer('background-video.mp4.mov')
    prefer('Create_a_subtle_202509101123.mp4')
    return () => {
      isMounted = false
    }
  }, [])

  return (
    <div className="video-background" aria-hidden>
      <video
        ref={videoRef}
        src={src}
        autoPlay
        muted
        loop
        playsInline
        preload="auto"
      />
    </div>
  )
}

