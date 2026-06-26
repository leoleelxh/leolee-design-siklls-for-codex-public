import { expect, test } from '@playwright/test';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const fixtureUrl = pathToFileURL(path.join(__dirname, 'fixtures', 'premium-landing.html')).toString();
const targetUrl = process.env.TARGET_URL || fixtureUrl;

test.describe('Agent Design visual QA', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(targetUrl, { waitUntil: 'networkidle' });
  });

  test('first viewport has clear composition and CTA', async ({ page }) => {
    await expect(page.locator('h1').first()).toBeVisible();
    await expect(page.locator('main').first()).toBeVisible();

    const primaryAction = page.locator('main a, main button, main [role="button"]').first();
    await expect(primaryAction).toBeVisible();

    const actionBox = await primaryAction.boundingBox();
    expect(actionBox, 'primary action should have a visible box').not.toBeNull();
    expect(actionBox!.y, 'primary action should appear in the first viewport').toBeLessThan(760);
  });

  test('layout does not overflow horizontally', async ({ page }) => {
    const overflow = await page.evaluate(() => {
      const doc = document.documentElement;
      return {
        viewport: window.innerWidth,
        documentWidth: Math.max(doc.scrollWidth, document.body.scrollWidth),
        offenders: Array.from(document.querySelectorAll<HTMLElement>('body *'))
          .map((node) => {
            const rect = node.getBoundingClientRect();
            return {
              tag: node.tagName.toLowerCase(),
              className: node.className.toString(),
              right: rect.right,
              left: rect.left
            };
          })
          .filter((item) => item.right > window.innerWidth + 2 || item.left < -2)
          .slice(0, 10)
      };
    });

    expect(overflow.documentWidth, JSON.stringify(overflow.offenders, null, 2)).toBeLessThanOrEqual(
      overflow.viewport + 2
    );
  });

  test('meaningful images expose alt text', async ({ page }) => {
    const missingAlt = await page.evaluate(() =>
      Array.from(document.querySelectorAll('img'))
        .filter((img) => !img.hasAttribute('alt'))
        .map((img) => img.getAttribute('src') || '[inline image]')
    );

    expect(missingAlt).toEqual([]);
  });

  test('interactive text has usable contrast against its surface', async ({ page }) => {
    const failures = await page.evaluate(() => {
      const parseRgb = (value: string): [number, number, number, number] | null => {
        const match = value.match(/rgba?\(([^)]+)\)/i);
        if (!match) return null;
        const parts = match[1].split(',').map((part) => Number.parseFloat(part.trim()));
        return [parts[0], parts[1], parts[2], parts[3] ?? 1];
      };

      const luminance = ([red, green, blue]: [number, number, number, number]) => {
        const convert = (channel: number) => {
          const value = channel / 255;
          return value <= 0.03928 ? value / 12.92 : Math.pow((value + 0.055) / 1.055, 2.4);
        };
        return 0.2126 * convert(red) + 0.7152 * convert(green) + 0.0722 * convert(blue);
      };

      const contrast = (a: [number, number, number, number], b: [number, number, number, number]) => {
        const light = Math.max(luminance(a), luminance(b));
        const dark = Math.min(luminance(a), luminance(b));
        return (light + 0.05) / (dark + 0.05);
      };

      const visibleButtons = Array.from(document.querySelectorAll<HTMLElement>('a, button, [role="button"]')).filter(
        (node) => node.offsetParent !== null && node.textContent?.trim()
      );

      return visibleButtons
        .map((node) => {
          const style = getComputedStyle(node);
          let background = parseRgb(style.backgroundColor);
          let parent: HTMLElement | null = node.parentElement;
          while (background && background[3] === 0 && parent) {
            background = parseRgb(getComputedStyle(parent).backgroundColor);
            parent = parent.parentElement;
          }
          const color = parseRgb(style.color);
          if (!color || !background) return null;
          const ratio = contrast(color, background);
          return {
            text: node.textContent?.trim(),
            ratio: Number(ratio.toFixed(2))
          };
        })
        .filter((item): item is { text: string; ratio: number } => Boolean(item) && item.ratio < 3);
    });

    expect(failures).toEqual([]);
  });
});
