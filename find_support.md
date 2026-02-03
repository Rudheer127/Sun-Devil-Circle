# **COMPLETE "FIND SUPPORT" FLOW - ULTRA-DETAILED UI SPECIFICATION**

Based on my comprehensive exploration of the SunDevil Circle website, here is the complete detailed specification for replicating the "Find Support" functionality: [sun-down-connect.lovable](https://sun-down-connect.lovable.app/)

***

## **🚀 FIND SUPPORT BUTTON - INITIAL INTERACTION**

### **Button Location & Styling**
**Position**: Hero section, center aligned, below subheadline text
```css
Background: Linear gradient(135deg, #8B1538, #A91D3A)
Color: #FFFFFF
Font-size: 18px
Font-weight: 600
Padding: 16px 40px
Border-radius: 28px (pill shape)
Border: none
Box-shadow: 0 8px 20px rgba(139, 21, 56, 0.3)
Display: Inline-flex
Align-items: Center
Gap: 8px
Cursor: pointer
Transition: all 300ms cubic-bezier(0.4, 0, 0.2, 1)
```

**Icon**: Right arrow (→) icon, 20px, white color

**Hover State**:
```css
Transform: translateY(-3px)
Box-shadow: 0 12px 28px rgba(139, 21, 56, 0.4)
Background: Linear gradient(135deg, #A91D3A, #C02446)
```

**Active/Click State**:
```css
Transform: translateY(-1px) scale(0.98)
Box-shadow: 0 6px 16px rgba(139, 21, 56, 0.35)
```

***

## **📋 SIGN-UP MODAL (First Screen After Click)**

### **Modal Container**
```css
Position: Fixed, centered (top: 50%, left: 50%, transform: translate(-50%, -50%))
Width: 480px (desktop), 90vw (mobile)
Max-width: 480px
Background: #FFFFFF
Border-radius: 24px
Box-shadow: 0 24px 48px rgba(0, 0, 0, 0.15)
Padding: 40px
Z-index: 9999
Animation: fadeIn 300ms ease-out, slideUp 300ms ease-out
```

**Background Overlay**:
```css
Position: Fixed
Top: 0, Left: 0, Right: 0, Bottom: 0
Background: rgba(0, 0, 0, 0.5)
Backdrop-filter: blur(4px)
Z-index: 9998
```

### **Modal Header**
**Title**: "Join the Circle"
```css
Font-size: 32px
Font-weight: 700
Color: #1A1A1A
Text-align: Center
Margin-bottom: 8px
```

**Subtitle**: "Create an account to find your support match"
```css
Font-size: 16px
Color: #6B7280
Text-align: Center
Margin-bottom: 32px
```

**Close Button (Top Right)**:
```css
Position: Absolute
Top: 16px
Right: 16px
Width: 32px
Height: 32px
Border: none
Background: transparent
Color: #9CA3AF
Cursor: pointer
Font-size: 24px
Hover: Color #4B5563, Background: #F3F4F6, Border-radius: 50%
```

### **Form Fields**

**Email Input**:
```css
Width: 100%
Height: 56px
Padding: 16px 16px 16px 48px
Border: 2px solid #E5E7EB
Border-radius: 12px
Font-size: 16px
Background: #FFFFFF
Margin-bottom: 16px
Transition: all 200ms ease

/* Icon (Email/Envelope) */
Position: Absolute
Left: 16px
Top: 18px
Width: 20px
Height: 20px
Color: #9CA3AF

/* Placeholder */
Placeholder: "your.email@asu.edu"
Color: #9CA3AF

/* Focus State */
Border-color: #8B1538
Box-shadow: 0 0 0 3px rgba(139, 21, 56, 0.1)
Outline: none

/* Filled State */
Border-color: #8B1538
```

**Password Input**:
```css
/* Same as email input, with additional features */
Width: 100%
Height: 56px
Padding: 16px 48px 16px 48px (space for lock icon left, eye icon right)
Border: 2px solid #E5E7EB
Border-radius: 12px
Font-size: 16px
Type: password (initially)
Margin-bottom: 24px

/* Lock Icon (Left) */
Position: Absolute
Left: 16px
Top: 18px
Width: 20px
Height: 20px
Color: #9CA3AF

/* Show/Hide Toggle (Right) */
Position: Absolute
Right: 16px
Top: 18px
Width: 20px
Height: 20px
Color: #9CA3AF
Cursor: pointer
Icon: Eye icon (shows password) / Eye-off icon (hides password)
On Click: Toggle input type between "password" and "text"
Hover: Color #4B5563
```

### **Create Account Button**
```css
Width: 100%
Height: 56px
Background: Linear gradient(135deg, #8B1538, #A91D3A)
Color: #FFFFFF
Font-size: 18px
Font-weight: 600
Border: none
Border-radius: 12px
Cursor: pointer
Display: Flex
Align-items: Center
Justify-content: Center
Gap: 8px
Transition: all 250ms ease
Margin-bottom: 20px

/* Icon */
Right arrow (→), 20px

/* Hover */
Background: Linear gradient(135deg, #A91D3A, #C02446)
Transform: translateY(-2px)
Box-shadow: 0 8px 16px rgba(139, 21, 56, 0.3)

/* Loading State (when clicked) */
Cursor: not-allowed
Opacity: 0.7
Content: Spinner animation (20px, white)
Text: Hidden
```

### **Sign In Link**
```css
Text-align: Center
Font-size: 15px
Color: #6B7280
Margin-bottom: 16px

/* Link Styling */
"Sign In" text:
  Color: #8B1538
  Font-weight: 600
  Text-decoration: none
  Hover: text-decoration underline
  Cursor: pointer
  Transition: all 200ms ease
```

### **Info Note**
```css
Display: Flex
Align-items: Center
Gap: 8px
Background: #FEF3C7
Padding: 12px 16px
Border-radius: 8px
Font-size: 14px
Color: #92400E

/* Icon (Light bulb emoji) */
💡 (emoji, 16px)

/* Text */
"ASU email addresses are recommended but not required"
```

***

## **🎯 ONBOARDING FLOW - 5 STEPS**

### **Progress Bar (Top of Each Step)**
```css
Position: Fixed or Absolute
Top: 0
Left: 0
Right: 0
Height: 4px
Background: #E5E7EB
Z-index: 100

/* Progress Fill */
Background: #8B1538
Height: 100%
Width: Calculated based on step (20%, 40%, 60%, 80%, 100%)
Transition: width 400ms ease-out
```

**Step Indicator Text**:
```css
Position: Absolute
Top: 24px
Right: 24px
Font-size: 14px
Color: #6B7280
Font-weight: 500
Text: "Step X of 5" (where X is current step)
```

***

## **STEP 1: SUPPORT TOPICS**

### **Container**
```css
Min-height: 100vh
Background: #FFFFFF
Padding: 80px 40px 120px
Display: Flex
Flex-direction: Column
Align-items: Center
```

### **Header Section**
**Title**: "What would you like support with?"
```css
Font-size: 36px
Font-weight: 700
Color: #1A1A1A
Text-align: Center
Margin-bottom: 12px
```

**Subtitle**: "Select all that apply"
```css
Font-size: 18px
Color: #6B7280
Text-align: Center
Margin-bottom: 48px
```

### **Topic Cards Grid**
```css
Display: Grid
Grid-template-columns: repeat(2, 1fr)
Gap: 16px
Max-width: 640px
Width: 100%
Margin: 0 auto
```

### **Individual Topic Card**
```css
Background: #FFFFFF
Border: 2px solid #E5E7EB
Border-radius: 16px
Padding: 24px
Display: Flex
Flex-direction: Column
Align-items: Center
Gap: 12px
Cursor: pointer
Transition: all 250ms ease
Min-height: 120px
Justify-content: Center

/* Hover State */
Border-color: #D1D5DB
Background: #F9FAFB
Transform: translateY(-2px)
Box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08)

/* Selected State */
Border-color: #8B1538
Border-width: 3px
Background: #FFF1F2
Box-shadow: 0 4px 16px rgba(139, 21, 56, 0.15)
Transform: scale(1.02)

/* Icon */
Font-size: 32px
Margin-bottom: 4px

/* Label */
Font-size: 16px
Font-weight: 600
Color: #1A1A1A
Text-align: Center
```

### **Topic Options** (with exact emoji icons):
1. **Homesickness** - 🏠 emoji
2. **Loneliness** - 💭 emoji
3. **Anxiety** - 😰 emoji
4. **Culture Shock** - 🌍 emoji
5. **Academics** - 📚 emoji
6. **Relationships** - 💕 emoji
7. **Identity** - 🪪 emoji
8. **Finances** - 💰 emoji
9. **Time Management** - ⏰ emoji

### **Continue Button (Bottom)**
```css
Position: Fixed
Bottom: 32px
Left: 50%
Transform: translateX(-50%)
Width: calc(100% - 80px)
Max-width: 600px
Height: 56px
Background: #8B1538
Color: #FFFFFF
Font-size: 18px
Font-weight: 600
Border: none
Border-radius: 12px
Display: Flex
Align-items: Center
Justify-content: Center
Gap: 8px
Cursor: pointer
Box-shadow: 0 8px 20px rgba(139, 21, 56, 0.3)
Transition: all 250ms ease
Z-index: 50

/* Disabled State (no topics selected) */
Background: #D1D5DB
Color: #9CA3AF
Cursor: not-allowed
Box-shadow: none
Opacity: 0.6

/* Hover (when enabled) */
Background: #A91D3A
Transform: translateX(-50%) translateY(-2px)
Box-shadow: 0 12px 28px rgba(139, 21, 56, 0.4)

/* Icon */
Right arrow (→), 20px
```

***

## **STEP 2: LANGUAGE & COMMUNICATION**

### **Header**
**Title**: "Language & Communication"
**Subtitle**: "Help us find the right match"

### **Section 1: Languages**
**Label**: "Languages you're comfortable with"
```css
Font-size: 16px
Font-weight: 600
Color: #1A1A1A
Margin-bottom: 16px
```

**Language Pills** (Multi-select):
```css
Display: Flex
Flex-wrap: Wrap
Gap: 12px
Margin-bottom: 40px
```

**Individual Language Pill**:
```css
Padding: 10px 20px
Border: 2px solid #E5E7EB
Border-radius: 24px (full pill)
Font-size: 15px
Font-weight: 500
Color: #4B5563
Background: #FFFFFF
Cursor: pointer
Transition: all 200ms ease

/* Hover */
Border-color: #D1D5DB
Background: #F9FAFB

/* Selected State */
Background: #8B1538
Color: #FFFFFF
Border-color: #8B1538
Font-weight: 600
```

**Language Options**:
- English, Spanish, Mandarin, Hindi, Arabic
- Portuguese, French, Korean, Japanese
- Vietnamese, Tagalog, Other

### **Section 2: Support Style**
**Label**: "How do you prefer to receive support?"

**Radio Card Options** (Single select):
```css
Display: Flex
Flex-direction: Column
Gap: 12px
Margin-bottom: 32px
```

**Individual Radio Card**:
```css
Background: #FFFFFF
Border: 2px solid #E5E7EB
Border-radius: 12px
Padding: 20px
Cursor: pointer
Transition: all 250ms ease

/* Hover */
Border-color: #D1D5DB
Background: #F9FAFB

/* Selected State */
Border-color: #8B1538
Border-width: 3px
Background: #FFF1F2
```

**Card Content**:
```css
/* Title */
Font-size: 16px
Font-weight: 600
Color: #1A1A1A
Margin-bottom: 4px

/* Description */
Font-size: 14px
Color: #6B7280
Line-height: 1.5
```

**Options**:
1. **Just listening**
   - "I prefer someone who listens without giving advice"

2. **Advice welcome**
   - "I appreciate suggestions and guidance"

3. **Mixed approach**
   - "Sometimes listening, sometimes advice"

### **Navigation Buttons (Bottom)**
```css
Display: Flex
Gap: 16px
Position: Fixed
Bottom: 32px
Left: 50%
Transform: translateX(-50%)
Width: calc(100% - 80px)
Max-width: 600px
Z-index: 50
```

**Back Button**:
```css
Width: 30%
Height: 56px
Background: #FFFFFF
Color: #4B5563
Font-size: 16px
Font-weight: 600
Border: 2px solid #E5E7EB
Border-radius: 12px
Display: Flex
Align-items: Center
Justify-content: Center
Gap: 8px
Cursor: pointer
Transition: all 250ms ease

/* Icon */
Left arrow (←), 20px

/* Hover */
Border-color: #8B1538
Color: #8B1538
Background: #FFF1F2
```

**Continue Button**:
```css
Flex: 1
/* Same styling as Step 1 Continue button */
```

***

## **STEP 3: YOUR PREFERENCES**

### **Header**
**Title**: "Your preferences"
**Subtitle**: "Optional — skip any you're unsure about"
```css
Color: #6B7280
Font-style: italic
```

### **Section 1: Cultural Background** (Optional)
**Label**: "Cultural background (optional)"

**Region Pills** (Multi-select):
- East Asia