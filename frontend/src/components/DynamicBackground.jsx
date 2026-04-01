import { Canvas } from '@react-three/fiber'
import { Sphere, useScroll } from '@react-three/drei'
import { useFrame, useThree } from '@react-three/fiber'
import { useRef, useMemo } from 'react'
import * as THREE from 'three'

const AnimatedSphere = ({ position, scale, color, speed }) => {
  const meshRef = useRef()

  useFrame(({ clock }) => {
    if (meshRef.current) {
      meshRef.current.rotation.x += speed * 0.001
      meshRef.current.rotation.y += speed * 0.0015
    }
  })

  return (
    <mesh ref={meshRef} position={position} scale={scale}>
      <icosahedronGeometry args={[1, 4]} />
      <meshPhongMaterial color={color} wireframe={true} emissive={color} emissiveIntensity={0.2} />
    </mesh>
  )
}

const FloatingParticles = () => {
  const groupRef = useRef()
  const particlesCount = 50

  const particles = useMemo(() => {
    const positions = new Float32Array(particlesCount * 3)
    for (let i = 0; i < particlesCount * 3; i += 3) {
      positions[i] = (Math.random() - 0.5) * 20
      positions[i + 1] = (Math.random() - 0.5) * 20
      positions[i + 2] = (Math.random() - 0.5) * 20
    }
    return positions
  }, [])

  useFrame(({ clock }) => {
    if (groupRef.current) {
      groupRef.current.rotation.x += 0.00005
      groupRef.current.rotation.y += 0.00008
    }
  })

  return (
    <group ref={groupRef}>
      <points>
        <bufferGeometry>
          <bufferAttribute attach="attributes-position" array={particles} count={particlesCount} itemSize={3} />
        </bufferGeometry>
        <pointsMaterial size={0.1} color="#d4af37" sizeAttenuation={true} />
      </points>
    </group>
  )
}

const Lights = () => (
  <>
    <ambientLight intensity={0.4} />
    <pointLight position={[10, 10, 10]} intensity={1} color="#d4af37" />
    <pointLight position={[-10, -10, -10]} intensity={0.8} color="#2dd4bf" />
  </>
)

export default function DynamicBackground() {
  return (
    <div style={{ width: '100%', height: '100%', position: 'absolute', top: 0, left: 0 }}>
      <Canvas camera={{ position: [0, 0, 15], fov: 75 }}>
        <Lights />
        <AnimatedSphere position={[5, 3, -5]} scale={2} color="#d4af37" speed={1} />
        <AnimatedSphere position={[-5, -3, -10]} scale={1.5} color="#2dd4bf" speed={0.8} />
        <FloatingParticles />
      </Canvas>
    </div>
  )
}
