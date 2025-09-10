export default function BackgroundVideo() {
  return (
    <div className="video-background" aria-hidden>
      <video
        src="/background.mp4"
        autoPlay
        muted
        loop
        playsInline
        preload="auto"
      />
    </div>
  )
}

