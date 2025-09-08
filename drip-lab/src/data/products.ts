import { Product } from '@/components/ProductCard';

export const products: Product[] = [
  // Rings
  {
    id: 'ring-001',
    name: 'Eternal Gold Ring',
    price: 1299,
    originalPrice: 1599,
    description: 'Exquisite 18k gold ring with brilliant cut diamond centerpiece. Handcrafted with precision and attention to detail.',
    category: 'ring',
    material: 'gold',
    image: '/images/ring-001.jpg',
    inStock: true,
    rating: 4.8,
    reviews: 127,
    tags: ['diamond', '18k gold', 'engagement', 'luxury']
  },
  {
    id: 'ring-002',
    name: 'Platinum Solitaire',
    price: 2499,
    description: 'Classic platinum solitaire ring featuring a 1-carat diamond. Timeless elegance for special moments.',
    category: 'ring',
    material: 'platinum',
    image: '/images/ring-002.jpg',
    inStock: true,
    rating: 4.9,
    reviews: 89,
    tags: ['diamond', 'platinum', 'solitaire', 'classic']
  },
  {
    id: 'ring-003',
    name: 'Silver Vintage Band',
    price: 399,
    description: 'Vintage-inspired sterling silver band with intricate filigree work. Perfect for everyday elegance.',
    category: 'ring',
    material: 'silver',
    image: '/images/ring-003.jpg',
    inStock: true,
    rating: 4.6,
    reviews: 203,
    tags: ['vintage', 'sterling silver', 'filigree', 'everyday']
  },

  // Necklaces
  {
    id: 'necklace-001',
    name: 'Golden Cascade',
    price: 1899,
    description: 'Stunning 18k gold necklace with cascading diamond drops. A statement piece for special occasions.',
    category: 'necklace',
    material: 'gold',
    image: '/images/necklace-001.jpg',
    inStock: true,
    rating: 4.7,
    reviews: 156,
    tags: ['diamond', '18k gold', 'statement', 'cascade']
  },
  {
    id: 'necklace-002',
    name: 'Platinum Pearl Strand',
    price: 3299,
    description: 'Luxurious platinum necklace with natural pearl strand. Sophisticated and elegant design.',
    category: 'necklace',
    material: 'platinum',
    image: '/images/necklace-002.jpg',
    inStock: true,
    rating: 4.9,
    reviews: 67,
    tags: ['pearl', 'platinum', 'strand', 'sophisticated']
  },
  {
    id: 'necklace-003',
    name: 'Silver Pendant',
    price: 599,
    description: 'Delicate sterling silver pendant with emerald accent. Perfect for adding a touch of color.',
    category: 'necklace',
    material: 'silver',
    image: '/images/necklace-003.jpg',
    inStock: true,
    rating: 4.5,
    reviews: 234,
    tags: ['emerald', 'sterling silver', 'pendant', 'colorful']
  },

  // Earrings
  {
    id: 'earrings-001',
    name: 'Diamond Studs',
    price: 899,
    description: 'Classic diamond stud earrings in 18k gold. Timeless elegance that never goes out of style.',
    category: 'earrings',
    material: 'gold',
    image: '/images/earrings-001.jpg',
    inStock: true,
    rating: 4.8,
    reviews: 189,
    tags: ['diamond', '18k gold', 'studs', 'classic']
  },
  {
    id: 'earrings-002',
    name: 'Platinum Drops',
    price: 1599,
    description: 'Elegant platinum drop earrings with sapphire accents. Perfect for evening wear.',
    category: 'earrings',
    material: 'platinum',
    image: '/images/earrings-002.jpg',
    inStock: true,
    rating: 4.7,
    reviews: 98,
    tags: ['sapphire', 'platinum', 'drops', 'evening']
  },
  {
    id: 'earrings-003',
    name: 'Silver Hoops',
    price: 299,
    description: 'Versatile sterling silver hoop earrings. From casual to formal, these work for any occasion.',
    category: 'earrings',
    material: 'silver',
    image: '/images/earrings-003.jpg',
    inStock: true,
    rating: 4.4,
    reviews: 312,
    tags: ['sterling silver', 'hoops', 'versatile', 'casual']
  },

  // Bracelets
  {
    id: 'bracelet-001',
    name: 'Gold Tennis Bracelet',
    price: 2199,
    description: 'Luxurious 18k gold tennis bracelet with brilliant cut diamonds. A true statement piece.',
    category: 'bracelet',
    material: 'gold',
    image: '/images/bracelet-001.jpg',
    inStock: true,
    rating: 4.9,
    reviews: 76,
    tags: ['diamond', '18k gold', 'tennis', 'statement']
  },
  {
    id: 'bracelet-002',
    name: 'Platinum Chain',
    price: 1299,
    description: 'Sleek platinum chain bracelet with diamond accents. Modern and sophisticated design.',
    category: 'bracelet',
    material: 'platinum',
    image: '/images/bracelet-002.jpg',
    inStock: true,
    rating: 4.6,
    reviews: 143,
    tags: ['diamond', 'platinum', 'chain', 'modern']
  },
  {
    id: 'bracelet-003',
    name: 'Silver Charm Bracelet',
    price: 499,
    description: 'Charming sterling silver bracelet with customizable charm options. Personal and meaningful.',
    category: 'bracelet',
    material: 'silver',
    image: '/images/bracelet-003.jpg',
    inStock: true,
    rating: 4.5,
    reviews: 267,
    tags: ['sterling silver', 'charms', 'customizable', 'personal']
  }
];

export const categories = [
  { id: 'all', name: 'All Products', count: products.length },
  { id: 'ring', name: 'Rings', count: products.filter(p => p.category === 'ring').length },
  { id: 'necklace', name: 'Necklaces', count: products.filter(p => p.category === 'necklace').length },
  { id: 'earrings', name: 'Earrings', count: products.filter(p => p.category === 'earrings').length },
  { id: 'bracelet', name: 'Bracelets', count: products.filter(p => p.category === 'bracelet').length },
];

export const materials = [
  { id: 'all', name: 'All Materials' },
  { id: 'gold', name: 'Gold' },
  { id: 'silver', name: 'Silver' },
  { id: 'platinum', name: 'Platinum' },
];

export const priceRanges = [
  { id: 'all', name: 'All Prices', min: 0, max: Infinity },
  { id: 'under-500', name: 'Under $500', min: 0, max: 500 },
  { id: '500-1000', name: '$500 - $1,000', min: 500, max: 1000 },
  { id: '1000-2000', name: '$1,000 - $2,000', min: 1000, max: 2000 },
  { id: 'over-2000', name: 'Over $2,000', min: 2000, max: Infinity },
];