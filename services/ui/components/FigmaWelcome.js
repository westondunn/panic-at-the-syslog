export default function FigmaWelcome() {
  return (
    <section
      className="min-h-[850px] overflow-hidden rounded-card border border-primary-100 bg-surface shadow-card"
      data-node-id="6025:84652"
    >
      <div className="flex min-h-[850px] flex-col xl:flex-row" data-node-id="6025:84652">
        <aside
          className="flex w-full flex-col justify-between bg-[#e4e4e4] p-8 xl:w-[600px] xl:p-16"
          data-node-id="6668:151162"
        >
          <h1
            className="text-[clamp(3rem,9vw,5.5rem)] font-medium leading-[1.167] tracking-[-1.5px] text-[#212121]"
            style={{ fontFamily: '"Roboto Mono", "Courier New", monospace' }}
            data-node-id="6668:151172"
          >
            Welcome
          </h1>
          <div
            className="mt-12 flex items-center justify-between text-xs leading-[1.66] tracking-[0.4px] text-text-secondary"
            data-node-id="6668:151174"
          >
            <span data-node-id="6668:151175">© mui.com</span>
            <span data-node-id="6668:151176">MUI for Figma Material UI v7.2.0</span>
          </div>
        </aside>

        <div className="flex flex-1 flex-col gap-12 p-8 xl:p-16" data-node-id="6025:84654">
          <section className="space-y-4 text-text-secondary" data-node-id="6333:151775">
            <h2
              className="text-[32px] leading-[1.235] tracking-[0.25px] text-[#212121]"
              data-node-id="6333:151776"
            >
              Welcome, Designer.
            </h2>
            <p className="text-base leading-[1.5] tracking-[0.15px]" data-node-id="6333:151777">
              You&apos;re currently exploring the community version of our
              library. Think of it as a fantastic test drive.
            </p>
            <div className="text-base leading-[1.5] tracking-[0.15px]" data-node-id="6721:19507">
              <p>Community Version (This file):</p>
              <ul className="list-disc pl-6">
                <li>
                  Best for: Quickly assembling screens with pre-built
                  instances.
                </li>
                <li>The deal: You can use everything as-is.</li>
              </ul>
            </div>
            <div className="text-base leading-[1.5] tracking-[0.15px]" data-node-id="6721:19508">
              <p>Full Version (The upgrade):</p>
              <ul className="list-disc pl-6">
                <li>
                  Best for: Building a custom design system and full-scale
                  products.
                </li>
                <li>
                  The deal: You get all the source components to customize
                  colors, typography, enable Dark Mode, and access the complete
                  1,500+ component inventory
                </li>
              </ul>
            </div>
          </section>

          <section className="space-y-4" data-node-id="6025:93849">
            <h2
              className="text-[32px] leading-[1.235] tracking-[0.25px] text-[#212121]"
              data-node-id="6025:93844"
            >
              Preview the full version
            </h2>
            <div className="rounded border border-primary-100 bg-surface p-6" data-node-id="6025:84903">
              <div className="flex flex-col gap-4 sm:flex-row" data-node-id="6025:84895">
                <a
                  className="inline-flex items-center justify-center rounded border border-[#90caf9] px-[22px] py-2 text-[15px] font-medium uppercase leading-[26px] tracking-[0.46px] text-[#1976d2] underline"
                  href="https://mui.com/r/material-ui-figma-latest"
                  target="_blank"
                  rel="noreferrer"
                  data-node-id="6025:84847"
                >
                  Preview the full Material UI library
                </a>
                <p
                  className="inline-flex items-center justify-center rounded border border-[#ce93d8] px-[22px] py-2 text-[15px] font-medium uppercase leading-[26px] tracking-[0.46px] text-[#9c27b0] no-underline"
                  data-node-id="6667:145060"
                >
                  Preview the full Joy UI library
                </p>
              </div>
            </div>
          </section>

          <section className="space-y-4 text-text-secondary" data-node-id="6025:93850">
            <h2
              className="text-[32px] leading-[1.235] tracking-[0.25px] text-[#212121]"
              data-node-id="6025:93845"
            >
              So, what&apos;s the catch?
            </h2>
            <p className="text-base leading-[1.5] tracking-[0.15px]" data-node-id="6025:93847">
              There isn&apos;t one, really. This version is for straightforward
              design work. But if you&apos;re looking to do the heavy
              lifting, like customizing colors, tweaking typography, or flipping
              on Dark Mode, you&apos;ll need the keys to the full library:{" "}
              <a
                className="underline"
                href="https://mui.com/store/items/figma-react/"
                target="_blank"
                rel="noreferrer"
              >
                https://mui.com/store/items/figma-react/
              </a>
            </p>
            <p className="text-base leading-[1.5] tracking-[0.15px]" data-node-id="6025:93847:tail">
              The Full Version gives you just that: access to all source
              components. It&apos;s the entire collection of over 1,500
              elements, ready for you to make completely your own.
            </p>
          </section>
        </div>
      </div>
    </section>
  );
}
