-- pdf_filter.lua — pandoc filter for the gauge paper's PDF (used by build_v6_4_pdf.py). It changes layout only.
-- 1. FreeSerif's bold and italic faces lack the double-struck letters ℂ ℍ ℝ ℤ 𝔽 𝕆 𝕊 and the bold digits 𝟏 𝟑 𝟕 𝟖.
--    Each of these characters is set in upright FreeSerif (\dsfont), which has them, so no glyph is dropped in bold or
--    italic text.
-- 2. FreeSerif has no mark anchor for digits, so a combining macron after a digit (the 3̄ of 3 ⊕ 3̄) is drawn at
--    lowercase height, inside the digit, and cannot be seen. A base followed by U+0304 is therefore set as the base
--    and the same macron glyph raised by 0.17 em and moved 0.1 em left, which puts it above the digit and centred.
--    The macron stays a real character, so copying 3̄ from the PDF still gives 3 and U+0304.
-- 3. A paragraph that is a single short italic span (the three displayed formulas, such as Q = N/3) is centered.
--    (Item 4, the ties, is below.)

local SPECIAL = {}
for _, cp in utf8.codes("ℂℍℝℤ𝔽𝕆𝕊𝟏𝟑𝟕𝟖") do SPECIAL[cp] = true end
local MACRON = 0x0304

local function is_combining(cp)
  return cp >= 0x0300 and cp <= 0x036F
end

function Str(el)
  local cps = {}
  for _, cp in utf8.codes(el.text) do cps[#cps + 1] = cp end
  local out, buf, i, changed = {}, {}, 1, false
  local function flush()
    if #buf > 0 then out[#out + 1] = pandoc.Str(utf8.char(table.unpack(buf))); buf = {} end
  end
  while i <= #cps do
    local base, marks, j = cps[i], {}, i + 1
    while j <= #cps and is_combining(cps[j]) do marks[#marks + 1] = cps[j]; j = j + 1 end
    if #marks == 1 and marks[1] == MACRON then
      flush()
      out[#out + 1] = pandoc.RawInline("latex", "{\\dsfont " .. utf8.char(base) ..
        "\\raisebox{0.17em}{\\kern-0.1em " .. utf8.char(MACRON) .. "\\kern0.1em}}")
      changed = true
    elseif #marks > 0 then
      error("unexpected combining mark sequence in: " .. el.text)
    elseif SPECIAL[base] then
      flush()
      out[#out + 1] = pandoc.RawInline("latex", "{\\dsfont " .. utf8.char(base) .. "}")
      changed = true
    else
      buf[#buf + 1] = base
    end
    i = j
  end
  if not changed then return nil end
  flush()
  return out
end

-- 4. Ties: the space after "Section(s)", "Problem(s)" or "Conjecture(s)" becomes a non-breaking space when the next
--    word starts with a digit or "(", so a line never ends at "Open Problem" with "(i)." on the next one.
local TIE = { Section = true, Sections = true, Problem = true, Problems = true, Conjecture = true, Conjectures = true }

function Inlines(inlines)
  for k = 1, #inlines - 2 do
    local a, sp, b = inlines[k], inlines[k + 1], inlines[k + 2]
    if a.t == "Str" and TIE[(a.text:gsub("^%(", ""))] and (sp.t == "Space" or sp.t == "SoftBreak")
        and b.t == "Str" and b.text:match("^[%(%d]") then
      inlines[k + 1] = pandoc.Str("\u{00A0}")
    end
  end
  return inlines
end

function Para(el)
  if #el.content == 1 and el.content[1].t == "Emph" then
    local text = pandoc.utils.stringify(el)
    if utf8.len(text) < 100 and not text:match("^Revision note") then
      return { pandoc.RawBlock("latex", "\\begin{center}"), pandoc.Plain(el.content),
               pandoc.RawBlock("latex", "\\end{center}") }
    end
  end
  return nil
end
