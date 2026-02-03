Based on my exhaustive analysis of the SunDevil Circle website, here is the **COMPLETE ULTRA-DETAILED PROMPT** covering every single feature, component, and interaction: [sun-down-connect.lovable](https://sun-down-connect.lovable.app/)

***

# **SUNDEVIL CIRCLE - COMPLETE REPLICATION PROMPT**

## **🎯 PROJECT OVERVIEW**
Build a peer support matching platform for Arizona State University students to connect with trained peer supporters. The platform emphasizes privacy, cultural awareness, and safety while providing anonymous mental health peer support (not professional therapy).

***

## **🎨 DESIGN SYSTEM - EXACT SPECIFICATIONS**

### **Color Palette (Extracted)**
```css
/* Primary Colors */
--primary-maroon: #8B1538;
--primary-gold: #FFC627;

/* Background Gradients */
--bg-gradient-start: #FFF5F5; /* Light pink */
--bg-gradient-end: #F5EEE6; /* Cream beige */

/* Text Colors */
--text-primary: #1A1A1A; /* Almost black */
--text-secondary: #6B7280; /* Medium gray */
--text-light: #9CA3AF; /* Light gray */
--text-white: #FFFFFF;

/* UI Element Colors */
--green-mint: #D1FAE5; /* Crisis banner background */
--green-accent: #10B981; /* Icons in green cards */
--pink-light: #FDE2E4; /* Badge background */
--pink-rose: #E11D48; /* Dot in badge */
--yellow-soft: #FEF3C7; /* Yellow icon backgrounds */

/* Semantic Colors */
--shield-green: #86EFAC; /* Privacy/security icons */
--warning-yellow: #FBBF24; /* Alert icons */
--error-red: #EF4444;
--success-green: #22C55E;

/* Card/Modal Colors */
--card-white: #FFFFFF;
--overlay-dark: rgba(0, 0, 0, 0.5);
--border-gray: #E5E7EB;
```

### **Typography System**
```css
/* Font Family */
--font-primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;

/* Font Sizes */
--text-xs: 12px;
--text-sm: 14px;
--text-base: 16px;
--text-lg: 18px;
--text-xl: 20px;
--text-2xl: 24px;
--text-3xl: 30px;
--text-4xl: 36px;
--text-5xl: 48px;
--text-6xl: 60px;
--text-hero: 72px; /* Main headline */

/* Font Weights */
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;
--font-extrabold: 800;

/* Line Heights */
--leading-tight: 1.2;
--leading-normal: 1.5;
--leading-relaxed: 1.75;
```

### **Spacing System**
```css
--spacing-1: 4px;
--spacing-2: 8px;
--spacing-3: 12px;
--spacing-4: 16px;
--spacing-5: 20px;
--spacing-6: 24px;
--spacing-8: 32px;
--spacing-10: 40px;
--spacing-12: 48px;
--spacing-16: 64px;
--spacing-20: 80px;
--spacing-24: 96px;
--spacing-32: 128px;
```

### **Border Radius**
```css
--radius-sm: 4px;
--radius-md: 8px;
--radius-lg: 12px;
--radius-xl: 16px;
--radius-2xl: 24px;
--radius-full: 9999px;
```

### **Shadows**
```css
--shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
--shadow-md: 0 4px 6px rgba(0, 0, 0, 0.07);
--shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
--shadow-xl: 0 20px 25px rgba(0, 0, 0, 0.15);
--shadow-card: 0 2px 8px rgba(0, 0, 0, 0.08);
```

***

## **📐 LAYOUT & STRUCTURE - PIXEL PERFECT**

### **1. CRISIS ALERT BANNER (Top Fixed)**
**Position**: Fixed top, full width, above navigation
**Styling**:
```
Height: 60px
Background: Linear gradient (#D1FAE5 to #ECFDF5)
Border-bottom: 1px solid #A7F3D0
Z-index: 1000
Display: Flex, justify-content: center, align-items: center
Padding: 12px 24px
```

**Content Structure**:
- **Left Icon**: Shield icon (20x20px), color: #10B981
- **Text (Bold)**: "Need immediate support?" (16px, font-weight: 600)
- **Subtext**: "Tap to see crisis resources available 24/7" (14px, color: #6B7280)
- **Close Button (Right)**: X icon (20x20px), absolute right: 24px, cursor: pointer

**Interaction**:
- On click: Expands to show 4 crisis resource cards
- Animation: Slide down with 300ms ease-out
- Cards shown: 988 Lifeline, ASU Counseling, Crisis Text, Campus Police

**Expanded Crisis Panel**:
```
Height: Auto (240px when expanded)
Background: White
Shadow: 0 4px 12px rgba(0, 0, 0, 0.1)
Padding: 24px 40px
Grid: 2x2 (desktop), 1x4 (mobile)
```

**Each Crisis Card**:
```
Background: Light pink (#FFF1F2) or Light green (#F0FDF4)
Border-radius: 12px
Padding: 20px
Icon: Phone or message icon (32x32px)
Title: Bold, 18px
Description: 14px, gray
Action Link: Maroon color, font-weight: 600, underline on hover
```

**Crisis Resources Shown**:
1. **988 Suicide & Crisis Lifeline**
   - Icon: Phone (red)
   - Text: "Free, confidential 24/7 support"
   - Action: "Call or text 988"
   - Background: #FFF1F2

2. **ASU Counseling Services**
   - Icon: Chat bubble (green)
   - Text: "Free mental health support for students"
   - Action: "Call (480) 965-6146"
   - Background: #F0FDF4

3. **Crisis Text Line**
   - Icon: Message (red)
   - Text: "Text-based crisis support"
   - Action: "Text HOME to 741741"
   - Background: #FFF1F2

4. **ASU Campus Police**
   - Icon: Phone (red)
   - Text: "For immediate safety concerns"
   - Action: "Call (480) 965-3456"
   - Background: #FFF1F2

***

### **2. NAVIGATION BAR (Sticky)**
**Position**: Fixed top (below crisis banner when shown), full width
**Styling**:
```
Height: 80px
Background: rgba(255, 255, 255, 0.95)
Backdrop-filter: blur(10px)
Border-bottom: 1px solid rgba(0, 0, 0, 0.05)
Z-index: 999
Box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04)
```

**Layout**: 
```
Container max-width: 1280px
Display: Flex
Justify-content: space-between
Align-items: center
Padding: 0 40px
```

**Components**:

**A. Logo (Left)**
```
Display: Flex, align-items: center
Gap: 8px
```
- **Icon**: Circular maroon background (40x40px) with white devil trident icon
- **Text**: 
  - "SunDevil" (20px, color: #8B1538, font-weight: 700)
  - "Circle" (20px, color: #FFC627, font-weight: 700)
- Both on same line, no line break

**B. Navigation Links (Center)**
```
Display: Flex
Gap: 32px
Font-size: 16px
Font-weight: 500
Color: #4B5563
```
Links:
1. "How It Works" - href="#how-it-works"
2. "Safety" - href="#safety"
3. "For Supporters" - href="#"

**Hover Effect**:
```
Color: #8B1538
Transition: color 200ms ease
Underline: 2px solid #8B1538 (appears from center)
```

**C. Action Buttons (Right)**
```
Display: Flex
Gap: 12px
```

**Sign In Button**:
```
Background: Transparent
Color: #4B5563
Font-weight: 500
Padding: 10px 20px
Border: none
Border-radius: 8px
Hover: Background #F3F4F6
Transition: all 200ms ease
Cursor: pointer
```

**Get Started Button**:
```
Background: Linear gradient(135deg, #8B1538, #A91D3A)
Color: #FFFFFF
Font-weight: 600
Padding: 12px 28px
Border: none
Border-radius: 24px (pill shape)
Box-shadow: 0 4px 12px rgba(139, 21, 56, 0.25)
Hover: Transform: translateY(-2px), Shadow: 0 6px 16px rgba(139, 21, 56, 0.35)
Transition: all 250ms ease
Cursor: pointer
```

***

### **3. HERO SECTION**

**Container**:
```
Min-height: 100vh (minus nav height)
Background: Linear gradient(180deg, #FFF5F5 0%, #F5EEE6 100%)
Position: Relative
Overflow: Hidden
Padding: 120px 40px 80px
```

**Background Image**:
```
Position: Absolute, bottom: 0, left: 0, right: 0
Image: Students sitting together in desert/ASU campus setting
Opacity: 0.7
Filter: Saturate(0.8)
Object-fit: Cover
Height: 60%
Overlay: Linear gradient(to top, transparent, rgba(255, 245, 245, 0.9) 50%)
```

**Content Container**:
```
Max-width: 1200px
Margin: 0 auto
Z-index: 10
Position: Relative
Text-align: Center
```

**Elements (Top to Bottom)**:

**A. Badge**:
```
Display: Inline-flex
Align-items: Center
Gap: 8px
Background: #FDE2E4
Padding: 8px 20px
Border-radius: 24px (full pill)
Margin-bottom: 32px
```
- **Dot**: 8px circle, background: #E11D48
- **Text**: "Peer Support for ASU Students" (14px, color: #8B1538, font-weight: 500)

**B. Main Headline**:
```
Font-size: 72px (desktop), 48px (tablet), 36px (mobile)
Font-weight: 800
Line-height: 1.1
Margin-bottom: 24px
```
- Line 1: "You're not alone." (Color: #1A1A1A)
- Line 2: "Find your circle." (Color: #8B1538)

**C. Subheadline**:
```
Font-size: 20px (desktop), 18px (mobile)
Color: #6B7280
Line-height: 1.6
Max-width: 700px
Margin: 0 auto 48px
```
Text: "Connect with trained peer supporters who understand your journey. Safe, confidential, and culturally-aware support — made for international students."

**D. CTA Buttons Container**:
```
Display: Flex
Gap: 16px
Justify-content: Center
Flex-wrap: Wrap
Margin-bottom: 64px
```

**Find Support Button (Primary)**:
```
Background: Linear gradient(135deg, #8B1538, #A91D3A)
Color: #FFFFFF
Font-size: 18px
Font-weight: 600
Padding: 16px 40px
Border-radius: 28px
Border: none
Box-shadow: 0 8px 20px rgba(139, 21, 56, 0.3)
Display: Inline-flex
Align-items: Center
Gap: 8px
Cursor: pointer
Transition: all 300ms ease
```
- **Icon**: Arrow right (→), 20px
- **Hover**: Transform: translateY(-3px), Shadow: 0 12px 28px rgba(139, 21, 56, 0.4)
- **Active**: Transform: translateY(-1px)

**Become a Supporter Button (Secondary)**:
```
Background: #FFFFFF
Color: #8B1538
Font-size: 18px
Font-weight: 600
Padding: 16px 40px
Border-radius: 28px
Border: 2px solid #8B1538
Box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08)
Cursor: pointer
Transition: all 300ms ease
```
- **Hover**: Background: #8B1538, Color: #FFFFFF, Transform: translateY(-3px)

**E. Feature Pills (Bottom)**:
```
Display: Flex
Gap: 24px
Justify-content: Center
Flex-wrap: Wrap
Position: Absolute
Bottom: 80px
Left: 50%
Transform: translateX(-50%)
```

**Each Pill**:
```
Background: rgba(255, 255, 255, 0.9)
Backdrop-filter: blur(8px)
Padding: 12px 24px
Border-radius: 24px
Display: Flex
Align-items: Center
Gap: 10px
Box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1)
```

Pills:
1. **Privacy-First**: Shield icon (green), text (14px, #4B5563)
2. **Trained Peers**: Users icon (maroon), text
3. **