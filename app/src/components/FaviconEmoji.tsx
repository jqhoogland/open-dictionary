/** Convert an emoji to a valid data url to include in a <link/> element */
export const getIconHref = (emoji: string): string => `data:image/svg+xml,
<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22>
  <text y=%22.9em%22 font-size=%2290%22>${emoji}</text>
</svg>`;

const FaviconEmoji: React.FC<{ children: string }> = ({ children }) => (
  <link rel="icon" href={getIconHref(children)} />
);

export default FaviconEmoji;
