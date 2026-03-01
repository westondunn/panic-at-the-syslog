import {
  FigmaBody,
  FigmaCtaRow,
  FigmaH4,
  FigmaInfoList,
  FigmaLeftPanel,
  FigmaOutlinedLabelCta,
  FigmaOutlinedLinkCta,
  FigmaPanelFooter,
  FigmaPageFrame,
  FigmaRightPanel,
  FigmaRichTextBlock,
  FigmaSection,
  FigmaSplitLayout,
} from "./figma/FigmaPrimitives";

export default function FigmaWelcome() {
  return (
    <FigmaPageFrame nodeId="6025:84652">
      <FigmaSplitLayout nodeId="6025:84652">
        <FigmaLeftPanel nodeId="6668:151162">
          <h1
            className="text-[clamp(3rem,9vw,5.5rem)] font-medium leading-[1.167] tracking-[-1.5px] text-[#212121]"
            style={{ fontFamily: '"Roboto Mono", "Courier New", monospace' }}
            data-node-id="6668:151172"
          >
            Welcome
          </h1>
          <FigmaPanelFooter
            left={"\u00A9 mui.com"}
            right="MUI for Figma Material UI v7.2.0"
            nodeId="6668:151174"
            leftNodeId="6668:151175"
            rightNodeId="6668:151176"
          />
        </FigmaLeftPanel>

        <FigmaRightPanel nodeId="6025:84654">
          <FigmaSection className="space-y-4 text-text-secondary" nodeId="6333:151775">
            <FigmaH4 nodeId="6333:151776">Welcome, Designer.</FigmaH4>
            <FigmaBody nodeId="6333:151777">
              You&apos;re currently exploring the community version of our
              library. Think of it as a fantastic test drive.
            </FigmaBody>
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
            <FigmaH4 nodeId="6025:93845">
              So, what&apos;s the catch?
            </FigmaH4>
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
        </FigmaRightPanel>
      </FigmaSplitLayout>
    </FigmaPageFrame>
  );
}

