'use client';

import { Suspense, useRef, useState } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Environment } from '@react-three/drei';
import { motion } from 'framer-motion';
import * as THREE from 'three';

// Ring component
function Ring({ position = [0, 0, 0], material = 'gold' }: { position?: [number, number, number], material?: 'gold' | 'silver' | 'platinum' }) {
  const meshRef = useRef<THREE.Mesh>(null);
  
  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.rotation.y = Math.sin(state.clock.elapsedTime * 0.5) * 0.1;
    }
  });

  const getMaterial = () => {
    switch (material) {
      case 'gold':
        return <meshStandardMaterial color="#ffd700" metalness={0.8} roughness={0.2} />
      case 'silver':
        return <meshStandardMaterial color="#c0c0c0" metalness={0.9} roughness={0.1} />
      case 'platinum':
        return <meshStandardMaterial color="#e5e4e2" metalness={0.7} roughness={0.3} />
      default:
        return <meshStandardMaterial color="#ffd700" metalness={0.8} roughness={0.2} />
    }
  };

  return (
    <group position={position}>
      {/* Ring band */}
      <mesh ref={meshRef}>
        <torusGeometry args={[1, 0.1, 16, 32]} />
        {getMaterial()}
      </mesh>
      
      {/* Diamond/Gem */}
      <mesh position={[0, 0, 0.8]}>
        <octahedronGeometry args={[0.3, 0]} />
        <meshStandardMaterial 
          color="#ffffff" 
          metalness={0.1} 
          roughness={0.1}
          transparent
          opacity={0.9}
        />
      </mesh>
    </group>
  );
}

// Necklace component
function Necklace({ position = [0, 0, 0], material = 'gold' }: { position?: [number, number, number], material?: 'gold' | 'silver' | 'platinum' }) {
  const groupRef = useRef<THREE.Group>(null);
  
  useFrame((state) => {
    if (groupRef.current) {
      groupRef.current.rotation.y = Math.sin(state.clock.elapsedTime * 0.3) * 0.05;
    }
  });

  const getMaterial = () => {
    switch (material) {
      case 'gold':
        return <meshStandardMaterial color="#ffd700" metalness={0.8} roughness={0.2} />
      case 'silver':
        return <meshStandardMaterial color="#c0c0c0" metalness={0.9} roughness={0.1} />
      case 'platinum':
        return <meshStandardMaterial color="#e5e4e2" metalness={0.7} roughness={0.3} />
      default:
        return <meshStandardMaterial color="#ffd700" metalness={0.8} roughness={0.2} />
    }
  };

  return (
    <group ref={groupRef} position={position}>
      {/* Chain links */}
      {Array.from({ length: 20 }, (_, i) => {
        const angle = (i / 20) * Math.PI * 2;
        const radius = 1.5;
        const x = Math.cos(angle) * radius;
        const z = Math.sin(angle) * radius;
        const y = Math.sin(angle * 2) * 0.3;
        
        return (
          <mesh key={i} position={[x, y, z]}>
            <torusGeometry args={[0.05, 0.02, 8, 16]} />
            {getMaterial()}
          </mesh>
        );
      })}
      
      {/* Pendant */}
      <mesh position={[0, -0.5, 0]}>
        <octahedronGeometry args={[0.4, 0]} />
        <meshStandardMaterial 
          color="#ffffff" 
          metalness={0.1} 
          roughness={0.1}
          transparent
          opacity={0.9}
        />
      </mesh>
    </group>
  );
}

// Bracelet component
function Bracelet({ position = [0, 0, 0], material = 'gold' }: { position?: [number, number, number], material?: 'gold' | 'silver' | 'platinum' }) {
  const groupRef = useRef<THREE.Group>(null);
  
  useFrame((state) => {
    if (groupRef.current) {
      groupRef.current.rotation.y = Math.sin(state.clock.elapsedTime * 0.3) * 0.1;
    }
  });

  const getMaterial = () => {
    switch (material) {
      case 'gold':
        return <meshStandardMaterial color="#ffd700" metalness={0.8} roughness={0.2} />
      case 'silver':
        return <meshStandardMaterial color="#c0c0c0" metalness={0.9} roughness={0.1} />
      case 'platinum':
        return <meshStandardMaterial color="#e5e4e2" metalness={0.7} roughness={0.3} />
      default:
        return <meshStandardMaterial color="#ffd700" metalness={0.8} roughness={0.2} />
    }
  };

  return (
    <group ref={groupRef} position={position}>
      {/* Bracelet band */}
      <mesh>
        <torusGeometry args={[1.2, 0.08, 16, 32]} />
        {getMaterial()}
      </mesh>
      
      {/* Decorative elements */}
      {Array.from({ length: 8 }, (_, i) => {
        const angle = (i / 8) * Math.PI * 2;
        const radius = 1.2;
        const x = Math.cos(angle) * radius;
        const z = Math.sin(angle) * radius;
        
        return (
          <mesh key={i} position={[x, 0, z]}>
            <sphereGeometry args={[0.05, 8, 8]} />
            {getMaterial()}
          </mesh>
        );
      })}
    </group>
  );
}

// Earrings component
function Earrings({ position = [0, 0, 0], material = 'gold' }: { position?: [number, number, number], material?: 'gold' | 'silver' | 'platinum' }) {
  const groupRef = useRef<THREE.Group>(null);
  
  useFrame((state) => {
    if (groupRef.current) {
      groupRef.current.rotation.y = Math.sin(state.clock.elapsedTime * 0.4) * 0.1;
    }
  });

  const getMaterial = () => {
    switch (material) {
      case 'gold':
        return <meshStandardMaterial color="#ffd700" metalness={0.8} roughness={0.2} />
      case 'silver':
        return <meshStandardMaterial color="#c0c0c0" metalness={0.9} roughness={0.1} />
      case 'platinum':
        return <meshStandardMaterial color="#e5e4e2" metalness={0.7} roughness={0.3} />
      default:
        return <meshStandardMaterial color="#ffd700" metalness={0.8} roughness={0.2} />
    }
  };

  return (
    <group ref={groupRef} position={position}>
      {/* Left earring */}
      <group position={[-0.8, 0, 0]}>
        <mesh>
          <sphereGeometry args={[0.1, 16, 16]} />
          {getMaterial()}
        </mesh>
        <mesh position={[0, -0.3, 0]}>
          <octahedronGeometry args={[0.2, 0]} />
          <meshStandardMaterial 
            color="#ffffff" 
            metalness={0.1} 
            roughness={0.1}
            transparent
            opacity={0.9}
          />
        </mesh>
      </group>
      
      {/* Right earring */}
      <group position={[0.8, 0, 0]}>
        <mesh>
          <sphereGeometry args={[0.1, 16, 16]} />
          {getMaterial()}
        </mesh>
        <mesh position={[0, -0.3, 0]}>
          <octahedronGeometry args={[0.2, 0]} />
          <meshStandardMaterial 
            color="#ffffff" 
            metalness={0.1} 
            roughness={0.1}
            transparent
            opacity={0.9}
          />
        </mesh>
      </group>
    </group>
  );
}

// Main 3D Scene
function Scene({ jewelryType, material }: { jewelryType: 'ring' | 'necklace' | 'earrings' | 'bracelet', material: 'gold' | 'silver' | 'platinum' }) {
  return (
    <>
      <ambientLight intensity={0.4} />
      <directionalLight position={[10, 10, 5]} intensity={1} />
      <pointLight position={[-10, -10, -5]} intensity={0.5} color="#d4af37" />
      
      {jewelryType === 'ring' && <Ring material={material} />}
      {jewelryType === 'necklace' && <Necklace material={material} />}
      {jewelryType === 'earrings' && <Earrings material={material} />}
      {jewelryType === 'bracelet' && <Bracelet material={material} />}
      
      <Environment preset="studio" />
      <OrbitControls 
        enablePan={false} 
        enableZoom={true} 
        enableRotate={true}
        minPolarAngle={Math.PI / 6}
        maxPolarAngle={Math.PI - Math.PI / 6}
      />
    </>
  );
}

// Loading component
function Loading() {
  return (
    <div className="w-full h-full flex items-center justify-center">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
    </div>
  );
}

// Main component
interface Jewelry3DProps {
  jewelryType: 'ring' | 'necklace' | 'earrings' | 'bracelet';
  material?: 'gold' | 'silver' | 'platinum';
  className?: string;
}

const Jewelry3D: React.FC<Jewelry3DProps> = ({ 
  jewelryType, 
  material = 'gold', 
  className = '' 
}) => {
  const [isLoaded, setIsLoaded] = useState(false);

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5 }}
      className={`relative ${className}`}
    >
      <div className="w-full h-full bg-gradient-to-br from-secondary to-accent rounded-lg overflow-hidden">
        <Canvas
          camera={{ position: [0, 0, 5], fov: 50 }}
          onCreated={() => setIsLoaded(true)}
        >
          <Suspense fallback={null}>
            <Scene jewelryType={jewelryType} material={material} />
          </Suspense>
        </Canvas>
        
        {!isLoaded && (
          <div className="absolute inset-0 flex items-center justify-center">
            <Loading />
          </div>
        )}
      </div>
    </motion.div>
  );
};

export default Jewelry3D;