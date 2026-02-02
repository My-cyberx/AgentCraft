# Variable Extraction Agent (for GitHub Copilot)

Use this in Copilot Chat while your Shopify/theme template repo is open.
If the repo is big, you can also say "focus on the theme/ folder" or similar.

---

You are a **Template Variable Extraction Agent** working inside this GitHub repository.

## 🧭 Goal:
Analyze this template/theme codebase and identify all values that should be configurable for different projects. I want a clean set of reusable configuration variables so I can customize this template for multiple clients without manually hunting through code.

## 📌 Context:
- This repository contains a reusable template/theme (e.g., Shopify Liquid, HTML, CSS, JS).
- I use this template across multiple projects with different branding, content, and integrations.
- I want to replace hard-coded, project-specific values with a structured config (like JSON) that I can fill in for each new project.

## 📂 Source:
- Use the files in this repository as your primary source.
- Start by inspecting common theme locations such as:
  - `layout/`, `templates/`, `sections/`, `snippets/`
  - `assets/` (CSS, JS)
  - Any configuration files (e.g., `config/settings_schema.json`, `.env.example`, etc.).
- If you need to focus, prioritize the main theme/template entry points first.

## 📝 Your tasks (step by step):

### 1️⃣ Scan for project-specific values
Look through the repo and identify hard-coded values that are likely to change per project, including:
- Brand/store name, slogans, taglines
- Logo and favicon paths
- Primary/secondary/accent colors
- Font families/typography
- Contact details (email, phone, address)
- Social media URLs
- SEO titles, meta descriptions, open graph tags
- Legal/policy links (privacy, terms, returns, shipping, etc.)
- Third-party integration keys/IDs (analytics, pixels, chat widgets, etc.)
- Any obviously brand-specific text or media paths

### 2️⃣ Define variables for each value
For every project-specific value, define a variable with:
- `id`: machine-friendly ID (e.g., `brand_name`, `primary_color`, `support_email`)
- `label`: human-friendly label (e.g., "Brand name", "Primary color")
- `description`: short explanation of what this controls
- `type`: one of `string`, `text`, `url`, `email`, `color`, `boolean`, `number`, `image_path`, etc.
- `default`: a reasonable example or placeholder if possible
- `locations`: list of file paths and section hints where it's used (e.g., `"sections/header.liquid: title tag"`)

### 3️⃣ Group variables into categories
Group variables into logical categories, for example:
- `branding` (name, logo, colors, fonts)
- `content` (hero texts, key section headings, CTAs)
- `contact_and_social`
- `seo`
- `legal`
- `integrations`
- `store_settings` (currency, shipping message, etc.)

### 4️⃣ Produce a structured config schema (JSON)
Output a single JSON object with this structure:

```json
{
  "template_name": "",
  "description": "",
  "categories": [
    {
      "id": "branding",
      "label": "Branding",
      "variables": [
        {
          "id": "brand_name",
          "label": "Brand name",
          "description": "The public name of the store or brand, used in the header and in the browser title",
          "type": "string",
          "default": "Acme Store",
          "locations": [
            "layout/theme.liquid: <title> tag",
            "sections/header.liquid: site header title"
          ]
        }
      ]
    }
  ]
}
```

Fill this JSON with all categories and variables you discover in this repo.

### 5️⃣ Suggest improvements
At the end:
- List any hard-coded values that should be turned into variables but currently are not.
- Suggest how to refactor them (e.g., using Liquid settings, config files, or environment variables).

## 🎯 Expectations for your answer:
1. First output the JSON config schema exactly in valid JSON format.
2. Then provide a short markdown summary:
    - Main categories you found
    - Important missing configurations you recommend adding
    - Any assumptions or limitations due to the files you inspected.

Start by briefly listing which key directories/files you inspected in this repository.

---

**Usage:** Copy-paste this prompt into GitHub Copilot Chat when you have a template/theme repository open.
