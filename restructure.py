import re

with open('mo-portfolio-v2/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

s_story = content.find('        <!-- ACT II')
s_journey = content.find('        <section id="journey"')
s_impact = content.find('        <!-- ACT III')
s_credentials = content.find('        <section id="credentials"')
s_philosophy = content.find('        <!-- ACT IV')

block_hero = content[:s_story]
block_story = content[s_story:s_journey]
block_journey = content[s_journey:s_impact]
block_impact = content[s_impact:s_credentials]
block_credentials = content[s_credentials:s_philosophy]
block_rest = content[s_philosophy:]

new_impact = block_impact.replace(
    '<span class="eyebrow">Expertise</span>',
    '<span class="eyebrow">Evidence-Backed Outcomes</span>'
).replace(
    '<h2 id="impact-heading">Skills &amp; Proficiencies</h2>',
    '<h2 id="impact-heading">Professional Impact</h2>\n                <p class="trust-signal" style="max-width: 65ch; margin-bottom: 2.5rem; font-size: 0.95rem; color: var(--text-secondary); line-height: 1.5;"><em>Every professional claim on this portfolio is linked to supporting documentation, verified qualifications, or documented professional evidence.</em></p>\n\n                <div class="impact-highlights" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; margin-bottom: 3.5rem;">\n                    <div class="impact-card" style="padding: 1.5rem; border: 1px solid var(--border); border-radius: 8px; background: var(--bg-secondary);">\n                        <h3 style="font-size: 1.1rem; margin-bottom: 0.75rem; display: flex; align-items: center; gap: 0.5rem;"><svg class="ic" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg> EAL &amp; Curriculum Design</h3>\n                        <p style="font-size: 0.9rem; color: var(--text-secondary); margin: 0;">Delivered curriculum-aligned EAL instruction across primary years, effectively bridging language acquisition with cross-curricular STEM and inquiry-based learning.</p>\n                    </div>\n                    <div class="impact-card" style="padding: 1.5rem; border: 1px solid var(--border); border-radius: 8px; background: var(--bg-secondary);">\n                        <h3 style="font-size: 1.1rem; margin-bottom: 0.75rem; display: flex; align-items: center; gap: 0.5rem;"><svg class="ic" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg> Teacher Mentoring</h3>\n                        <p style="font-size: 0.9rem; color: var(--text-secondary); margin: 0;">Directed Grade 5 writing moderation and mentored early-career teachers, standardizing assessment practices and ensuring high instructional consistency.</p>\n                    </div>\n                    <div class="impact-card" style="padding: 1.5rem; border: 1px solid var(--border); border-radius: 8px; background: var(--bg-secondary);">\n                        <h3 style="font-size: 1.1rem; margin-bottom: 0.75rem; display: flex; align-items: center; gap: 0.5rem;"><svg class="ic" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg> Instructional Quality</h3>\n                        <p style="font-size: 0.9rem; color: var(--text-secondary); margin: 0;">Designed and facilitated pedagogical professional development and quality assurance frameworks across international campuses (UK, Dubai, Malta).</p>\n                    </div>\n                </div>'
)

new_content = block_hero + new_impact + block_journey + block_credentials + block_story + block_rest

with open('mo-portfolio-v2/index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("HTML restructured.")
