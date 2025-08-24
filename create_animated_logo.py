#!/usr/bin/env python3
"""
LumiAI Animated Logo Generator
Creates an animated GIF with a moving light beam across LumiAI text
"""

from PIL import Image, ImageDraw, ImageFont
import math
import os

def create_animated_logo(output_path="animated_lumiai_logo.gif", 
                        width=600, height=300, 
                        fps=15, duration=3):
    """
    Create an animated logo with moving light beam effect
    
    Args:
        output_path: Output GIF file path
        width: Image width in pixels
        height: Image height in pixels
        fps: Frames per second
        duration: Animation duration in seconds
    """
    
    # Calculate total frames
    total_frames = int(fps * duration)
    
    # Create frames for the animation
    frames = []
    
    print(f"Creating {total_frames} frames for {duration}s animation at {fps} FPS...")
    
    for frame in range(total_frames):
        # Create base image with transparent background
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Calculate light beam position (moves from left to right)
        progress = frame / (total_frames - 1)
        beam_x = int(progress * width)
        
        # Draw background circle (similar to your logo)
        center_x, center_y = width // 2, height // 2
        circle_radius = min(width, height) // 3
        
        # Background circle with gradient effect
        for r in range(circle_radius, 0, -2):
            alpha = int(100 + (r / circle_radius) * 100)
            color = (26, 26, 46, alpha)  # Dark blue from your logo
            draw.ellipse([center_x - r, center_y - r, center_x + r, center_y + r], 
                        fill=color)
        
        # Draw LumiAI text
        try:
            # Try to use a system font, fallback to default if not available
            font_size = min(width, height) // 8
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
            except:
                try:
                    font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", font_size)
                except:
                    font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
        
        # Calculate text position
        text = "LumiAI"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = center_x - text_width // 2
        text_y = center_y + circle_radius // 3
        
        # Draw main text (white)
        draw.text((text_x, text_y), text, fill=(255, 255, 255, 255), font=font)
        
        # Draw animated light beam effect
        beam_width = width // 6  # Light beam width
        beam_intensity = 0.8
        
        for i in range(beam_width):
            # Calculate distance from beam center
            distance_from_center = abs(i - beam_width // 2)
            
            # Calculate alpha based on distance (gaussian falloff)
            alpha = int(255 * beam_intensity * math.exp(-(distance_from_center ** 2) / (beam_width // 4)))
            
            # Calculate x position
            x = beam_x + i - beam_width // 2
            
            if 0 <= x < width:
                # Create light beam with yellow color and glow effect
                # Main beam
                draw.line([(x, 0), (x, height)], fill=(255, 255, 0, alpha), width=3)
                
                # Glow effect (wider, more transparent)
                glow_alpha = alpha // 3
                draw.line([(x, 0), (x, height)], fill=(255, 255, 200, glow_alpha), width=7)
        
        # Add some sparkle effects
        if frame % 5 == 0:  # Every 5th frame
            sparkle_x = int(beam_x + (frame % 20 - 10))
            if 0 <= sparkle_x < width:
                # Draw sparkle
                sparkle_size = 4
                sparkle_alpha = 200
                draw.ellipse([sparkle_x - sparkle_size, center_y - sparkle_size,
                             sparkle_x + sparkle_size, center_y + sparkle_size], 
                            fill=(255, 255, 255, sparkle_alpha))
        
        frames.append(img)
        
        # Progress indicator
        if frame % 10 == 0:
            print(f"  Frame {frame}/{total_frames} ({frame/total_frames*100:.1f}%)")
    
    print("Saving animated GIF...")
    
    # Save as animated GIF
    frame_duration = int(1000 / fps)  # Duration in milliseconds
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=frame_duration,
        loop=0,  # Loop indefinitely
        optimize=True,
        quality=95
    )
    
    print(f"✅ Animated logo saved to: {output_path}")
    print(f"📊 Stats: {total_frames} frames, {fps} FPS, {duration}s duration")
    
    return output_path

def create_variations():
    """Create different variations of the animated logo"""
    
    # Main logo
    create_animated_logo("animated_lumiai_logo.gif", 600, 300, 15, 3)
    
    # Smaller version for web
    create_animated_logo("animated_lumiai_logo_small.gif", 300, 150, 15, 3)
    
    # Faster version
    create_animated_logo("animated_lumiai_logo_fast.gif", 600, 300, 24, 2)
    
    # Slower, smoother version
    create_animated_logo("animated_lumiai_logo_smooth.gif", 800, 400, 30, 4)

if __name__ == "__main__":
    print("🎨 LumiAI Animated Logo Generator")
    print("=" * 40)
    
    # Check if PIL/Pillow is available
    try:
        from PIL import Image, ImageDraw, ImageFont
        print("✅ PIL/Pillow is available")
    except ImportError:
        print("❌ PIL/Pillow not found. Installing...")
        os.system("pip3 install Pillow")
        try:
            from PIL import Image, ImageDraw, ImageFont
            print("✅ PIL/Pillow installed successfully")
        except ImportError:
            print("❌ Failed to install PIL/Pillow. Please install manually:")
            print("   pip3 install Pillow")
            exit(1)
    
    # Create the main animated logo
    create_animated_logo()
    
    print("\n🎉 Logo generation complete!")
    print("💡 You can now use the animated GIF in your:")
    print("   - GitHub README files")
    print("   - Project documentation")
    print("   - Social media posts")
    print("   - Presentations")
