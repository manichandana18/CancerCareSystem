export interface Wig {
  id: string;
  name: string;
  type: 'Synthetic' | 'Human Hair';
  color: string;
  price: number;
  imageUrl: string;
  verifiedSeller: boolean;
  description: string;
}

export const mockWigs: Wig[] = [
  {
    id: '1',
    name: 'Natural Black Bob',
    type: 'Human Hair',
    color: 'Black',
    price: 150,
    imageUrl: 'https://images.unsplash.com/photo-1595476108010-b4d1f102b1b1?auto=format&fit=crop&q=80&w=600',
    verifiedSeller: true,
    description: 'High-quality natural human hair wig, breathable cap.'
  },
  {
    id: '2',
    name: 'Golden Blonde Waves',
    type: 'Synthetic',
    color: 'Blonde',
    price: 80,
    imageUrl: 'https://images.unsplash.com/photo-1560889269-63c621183d29?auto=format&fit=crop&q=80&w=600',
    verifiedSeller: true,
    description: 'Heat-resistant synthetic fiber, looks natural.'
  },
  {
    id: '3',
    name: 'Chestnut Brown Long',
    type: 'Human Hair',
    color: 'Brown',
    price: 200,
    imageUrl: 'https://images.unsplash.com/photo-1522337660859-02fbefca4702?auto=format&fit=crop&q=80&w=600',
    verifiedSeller: true,
    description: 'Luxurious long brown hair, easy to style.'
  },
  {
    id: '4',
    name: 'Short Pixie Cut',
    type: 'Synthetic',
    color: 'Silver',
    price: 60,
    imageUrl: 'https://images.unsplash.com/photo-1635392769416-5655a6435c43?auto=format&fit=crop&q=80&w=600',
    verifiedSeller: true,
    description: 'Modern and chic pixie cut with comfortable lining.'
  },
  {
    id: '5',
    name: 'Auburn Shoulder Length',
    type: 'Human Hair',
    color: 'Auburn',
    price: 180,
    imageUrl: 'https://images.unsplash.com/photo-1580618672591-eb180b1a973f?auto=format&fit=crop&q=80&w=600',
    verifiedSeller: true,
    description: 'Soft texture with natural volume.'
  }
];
