import Link from 'next/link';
import { Instagram, Facebook, Twitter, Mail, Phone, MapPin } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="bg-secondary border-t border-border">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="col-span-1 md:col-span-2">
            <Link href="/" className="flex items-center space-x-2 mb-4">
              <div className="w-8 h-8 bg-gradient-to-br from-gold to-primary rounded-lg flex items-center justify-center">
                <span className="text-background font-bold text-lg">D</span>
              </div>
              <span className="text-xl font-bold gradient-text">Drip Lab</span>
            </Link>
            <p className="text-muted mb-4 max-w-md">
              Crafting exquisite jewelry pieces with precision and passion. 
              Each piece tells a story of luxury, elegance, and timeless beauty.
            </p>
            <div className="flex space-x-4">
              <a href="#" className="text-muted hover:text-primary transition-colors">
                <Instagram className="w-5 h-5" />
              </a>
              <a href="#" className="text-muted hover:text-primary transition-colors">
                <Facebook className="w-5 h-5" />
              </a>
              <a href="#" className="text-muted hover:text-primary transition-colors">
                <Twitter className="w-5 h-5" />
              </a>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-foreground font-semibold mb-4">Quick Links</h3>
            <ul className="space-y-2">
              <li>
                <Link href="/about" className="text-muted hover:text-primary transition-colors">
                  About Us
                </Link>
              </li>
              <li>
                <Link href="/collections" className="text-muted hover:text-primary transition-colors">
                  Collections
                </Link>
              </li>
              <li>
                <Link href="/custom" className="text-muted hover:text-primary transition-colors">
                  Custom Design
                </Link>
              </li>
              <li>
                <Link href="/care" className="text-muted hover:text-primary transition-colors">
                  Jewelry Care
                </Link>
              </li>
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h3 className="text-foreground font-semibold mb-4">Contact</h3>
            <ul className="space-y-2">
              <li className="flex items-center space-x-2 text-muted">
                <MapPin className="w-4 h-4" />
                <span>123 Jewelry Lane, Luxury District</span>
              </li>
              <li className="flex items-center space-x-2 text-muted">
                <Phone className="w-4 h-4" />
                <span>+1 (555) 123-4567</span>
              </li>
              <li className="flex items-center space-x-2 text-muted">
                <Mail className="w-4 h-4" />
                <span>info@driplab.com</span>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-border mt-8 pt-8 flex flex-col md:flex-row justify-between items-center">
          <p className="text-muted text-sm">
            © 2024 Drip Lab. All rights reserved.
          </p>
          <div className="flex space-x-6 mt-4 md:mt-0">
            <Link href="/privacy" className="text-muted hover:text-primary text-sm transition-colors">
              Privacy Policy
            </Link>
            <Link href="/terms" className="text-muted hover:text-primary text-sm transition-colors">
              Terms of Service
            </Link>
            <Link href="/shipping" className="text-muted hover:text-primary text-sm transition-colors">
              Shipping Info
            </Link>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;