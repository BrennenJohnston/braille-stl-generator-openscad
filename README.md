# Braille STL Generator (OpenSCAD)

> **⚠️ WORK IN PROGRESS**  
> This repository is currently under active development. The validation framework and test infrastructure are being implemented. The core OpenSCAD generator is functional, but automated testing and cross-platform validation are not yet complete. Expect breaking changes until v1.0.0 is officially released.

Parametric OpenSCAD program for generating braille embossing plates and counter plates for both flat cards and cylindrical objects.

## 🔗 Related Project

This is the **offline OpenSCAD companion** to the web-based Braille STL Generator:

| Version | Link | Use Case |
|---------|------|----------|
| **Web App** | [braille-card-and-cylinder-stl-gener.vercel.app](https://braille-card-and-cylinder-stl-gener.vercel.app) | Browser-based with automatic translation |
| **OpenSCAD** (this repo) | [github.com/BrennenJohnston/braille-stl-generator-openscad](https://github.com/BrennenJohnston/braille-stl-generator-openscad) | Offline use, full parametric control |
| **Web App Source** | [github.com/BrennenJohnston/braille-card-and-cylinder-stl-generator](https://github.com/BrennenJohnston/braille-card-and-cylinder-stl-generator) | Web app source code |

## ⚠️ Key Difference

**This OpenSCAD version requires pre-translated Unicode braille text.** It does NOT include automatic translation.

## 🚀 Quick Start

1. **Translate your text**:
   - Go to https://www.branah.com/braille-translator
   - Select Grade 1 or Grade 2 braille
   - Ensure "Unicode Braille" is selected (NOT ASCII)
   - Type your text and copy the braille output (e.g., ⠓⠑⠇⠇⠕)

2. **Open in OpenSCAD**:
   - Open `Braille_Card_And_Cylinder_STL_Generator.scad`
   - Open the Customizer panel (View → Customizer)

3. **Configure**:
   - Paste braille into `Line_1`, `Line_2`, etc.
   - Choose `shape_type`: `card` or `cylinder`
   - Choose `plate_type`: `positive` (emboss) or `negative` (counter)
   - Choose `combined_shape`: `rounded` or `cone`

4. **Generate**:
   - Render: F6 (or Design → Render)
   - Export: File → Export → Export as STL

## 📋 What This Makes

- **Card Emboss Plate**: Raised braille dots for flat cards
- **Card Counter Plate**: Recessed support for embossing flat cards
- **Cylinder Emboss Plate**: Raised dots on cylindrical surface
- **Cylinder Counter Plate**: Recessed support for cylindrical objects

## 🎯 Features

### Shape Options
- **Rounded**: Dome-shaped dots with spherical bowl recesses
- **Cone**: Traditional frustum cone dots with matching cone recesses

### Indicator Shapes
- Optional start/end markers for each row (toggle: `"on"` or `"off"`)
- Helps with plate alignment during embossing
- Reserves 2 cells per row when enabled (`indicator_shapes = "on"`)

### Parametric Control
All parameters match the web-based generator UI:
- Card dimensions (width, height, thickness)
- Cylinder dimensions (diameter, height, cutout)
- Braille spacing (cell, line, dot spacing)
- Dot dimensions (separate controls for rounded and cone shapes)
- Counter plate recess dimensions
- Positioning adjustments (X/Y offsets)

## 📐 Default Settings

All defaults match industry standards and web app defaults:

### Card Settings
- Width: 90mm (standard business card)
- Height: 52mm
- Thickness: 2mm

### Cylinder Settings
- Diameter: 30.75mm
- Height: 52mm
- Polygonal Cutout: 13mm radius, 12 points/sides
- Seam Offset: 355°

### Braille Grid
- Cells per row: 11 (available for text; 2 additional cells reserved when indicators are on)
- Number of rows: 4
- Cell spacing: 6.5mm
- Line spacing: 10.0mm
- Dot spacing: 2.5mm

### Dot Dimensions (Rounded - Default)
- Base diameter: 2.0mm
- Base height: 0.2mm
- Dome diameter: 1.5mm
- Dome height: 0.6mm

### Counter Plate (Bowl - Default)
- Base diameter: 1.8mm
- Depth: 0.8mm

## 🔧 Expert Mode Parameters

The Customizer organizes parameters into sections matching the web app:

1. **Text Input - Pre-Translated Braille**: Pre-translated braille lines
2. **Shape and Plate Selection**: Card/Cylinder, Emboss/Counter
3. **Expert Mode - Shape Selection**: Rounded/Cone, Indicator Shapes
4. **Expert Mode - Surface Dimensions**: Card and Cylinder dimensions combined
5. **Expert Mode - Braille Spacing**: Grid layout and positioning parameters
6. **Expert Mode - Braille Dot Adjustments**: 
   - Emboss Dot Dimensions (Rounded Shape)
   - Emboss Dot Dimensions (Cone Shape)
   - Counter Dot Dimensions (Rounded Shape / Bowl)
   - Counter Dot Dimensions (Cone Shape)
7. **Rendering Quality**: Mesh resolution settings

## 📊 Parameter Mapping

See [PARAMETER_MAPPING.md](PARAMETER_MAPPING.md) for complete mapping between OpenSCAD parameters and web app UI controls.

## 📐 Technical Specifications

For developers and contributors, detailed technical documentation is available:

- **[OPENSCAD_COORDINATE_SYSTEM_SPECIFICATIONS.md](OPENSCAD_COORDINATE_SYSTEM_SPECIFICATIONS.md)**: Coordinate system details, cylinder surface dot positioning, rotation/translation transformations, and centering logic for rounded dots.

## 🎓 Usage Examples

### Business Card (Flat Card)
```
1. Translate "John Doe\n555-1234" at Branah.com
2. Set shape_type = "card"
3. Set plate_type = "positive"
4. Set combined_shape = "rounded"
5. Paste braille into Line_1 and Line_2
6. Render and export
```

### Cylindrical Label
```
1. Translate your text at Branah.com
2. Set shape_type = "cylinder"
3. Set plate_type = "positive"
4. Adjust cylinder_diameter_mm as needed
5. Paste braille into lines
6. Render and export
```

### Universal Counter Plate
```
1. No text needed (creates all positions)
2. Set shape_type = "card" or "cylinder"
3. Set plate_type = "negative"
4. Set combined_shape to match your emboss plate
5. Render and export
```

## 🖨️ 3D Printing Tips

- **Material**: PLA works well; PETG is more durable
- **Layer Height**: 0.1-0.2mm for smooth dots
- **Infill**: 40%+ recommended for stiffness
- **Perimeters**: 3-4 for strength
- **Orientation**: 
  - Cards: Print flat, embossed surface UP
  - Cylinders: Print upright as oriented in preview
- **Speed**: Slower outer walls (≤30mm/s) for smoother dots

## 📚 References

1. **Web Generator**: https://braille-card-and-cylinder-stl-gener.vercel.app
2. **Branah Translator**: https://www.branah.com/braille-translator
3. **BANA Standards**: https://brailleauthority.org/size-and-spacing-braille-characters
4. **NLS Spec 800**: https://www.loc.gov/nls/
5. **ADA Standards**: https://archive.ada.gov/

## 🙏 Acknowledgments

- **Brennen Johnston**: Original web-based generator
- **Tobi Weinberg**: Project inception and development support
- **Liblouis**: Professional braille translation library (used in web app)

## 📄 License

This project is licensed under the **PolyForm Noncommercial License 1.0.0**.

- ✅ Free for personal, educational, and non-commercial use
- ✅ Modification and remixing allowed
- ❌ **No commercial use permitted**

See the [LICENSE](LICENSE) file for full terms.

## 🆚 Web App vs. OpenSCAD

### Use Web App When:
- ✅ You need automatic braille translation
- ✅ You want live 3D preview
- ✅ You prefer no software installation
- ✅ You need multi-language support (100+ tables)

### Use OpenSCAD When:
- ✅ You want to work offline
- ✅ You need full parametric control
- ✅ You want to modify/extend the code
- ✅ You have existing OpenSCAD workflows
- ✅ You need version control (plain text files)
- ✅ You want batch processing capability

## 🐛 Troubleshooting

### "INVALID CHARACTERS" Warning
- You pasted regular text instead of Unicode braille
- Solution: Translate at Branah.com and copy the braille output

### "TEXT TOO LONG" Warning
- Your braille text exceeds `grid_columns` limit
- Solution: Reduce text length or increase `grid_columns`

### Dots Don't Align
- Check `braille_x_adjust` and `braille_y_adjust`
- Ensure `cell_spacing`, `line_spacing`, and `dot_spacing` match between emboss and counter plates

### Plates Don't Fit Together
- Verify both plates use same `combined_shape` setting
- Check that counter plate dimensions match emboss dimensions
- Ensure `indicator_shapes` setting is same for both plates

## 📞 Support

For issues specific to this OpenSCAD version:
1. [Open an issue](https://github.com/BrennenJohnston/braille-stl-generator-openscad/issues) on this repository
2. Check parameter values in Customizer
3. Verify Unicode braille character validity
4. Ensure OpenSCAD version 2021.01 or newer

For general braille embossing questions, see the [web app](https://braille-card-and-cylinder-stl-gener.vercel.app).

---

**Version**: 1.0.0  
**Last Updated**: 2026-01-08
