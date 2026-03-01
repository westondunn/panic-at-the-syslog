import {
  FigmaCenteredCanvas,
  FigmaCtaRow,
  FigmaH4,
  FigmaInfoList,
  FigmaOutlinedLabelCta,
  FigmaOutlinedLinkCta,
  FigmaRichTextBlock,
  FigmaSection,
} from "./figma/FigmaPrimitives";

export default function FigmaWelcomeBox() {
  return (
    <FigmaCenteredCanvas nodeId="6025:84654">
      <FigmaSection className="space-y-4 text-text-secondary" nodeId="6333:151775">
        <FigmaH4 nodeId="6333:151776">Welcome, Designer.</FigmaH4>
        <p className="text-base leading-[1.5] tracking-[0.15px]" data-node-id="6333:151777">
          You&apos;re currently exploring the community version of our library.
          Think of it as a fantastic test drive.
        </p>
        <FigmaInfoList
          title="Community Version (This file):"
          nodeId="6721:19507"
          items={[
            "Best for: Quickly assembling screens with pre-built instances.",
            "The deal: You can use everything as-is.",
          ]}
        />
        <FigmaInfoList
          title="Full Version (The upgrade):"
          nodeId="6721:19508"
          items={[
            "Best for: Building a custom design system and full-scale products.",
            "The deal: You get all the source components to customize colors, typography, enable Dark Mode, and access the complete 1,500+ component inventory",
          ]}
        />
      </FigmaSection>

      <FigmaSection className="space-y-4" nodeId="6025:93849">
        <FigmaH4 nodeId="6025:93844">Preview the full version</FigmaH4>
        <FigmaCtaRow nodeId="6025:84903">
          <div className="flex flex-col gap-4 sm:flex-row" data-node-id="6025:84895">
            <FigmaOutlinedLinkCta
              href="https://mui.com/r/material-ui-figma-latest"
              nodeId="6025:84847"
              tone="primary"
            >
              Preview the full Material UI library
            </FigmaOutlinedLinkCta>
            <FigmaOutlinedLabelCta nodeId="6667:145060" tone="secondary">
              Preview the full Joy UI library
            </FigmaOutlinedLabelCta>
          </div>
        </FigmaCtaRow>
      </FigmaSection>

      <FigmaSection className="space-y-4 text-text-secondary" nodeId="6025:93850">
        <FigmaH4 nodeId="6025:93845">So, what&apos;s the catch?</FigmaH4>
        <FigmaRichTextBlock
          nodeId="6025:93847"
          paragraphs={[
            {
              id: "6025:93847:p1",
              parts: [
                {
                  type: "text",
                  text: "There isn't one, really. This version is for straightforward design work. But if you're looking to do the heavy lifting, like customizing colors, tweaking typography, or flipping on Dark Mode, you'll need the keys to the full library: ",
                },
                {
                  type: "link",
                  text: "https://mui.com/store/items/figma-react/",
                  href: "https://mui.com/store/items/figma-react/",
                },
              ],
            },
            {
              id: "6025:93847:p2",
              parts: [
                {
                  type: "text",
                  text: "The Full Version gives you just that: access to all source components. It's the entire collection of over 1,500 elements, ready for you to make completely your own.",
                },
              ],
            },
          ]}
        />
      </FigmaSection>
    </FigmaCenteredCanvas>
  );
}
