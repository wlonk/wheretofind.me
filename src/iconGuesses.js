function parseUrl(url) {
  const a = document.createElement('a');
  a.href = url;
  return a;
}

const iconGuesses = [
  { fn: () => true, val: 'fas fa-link' },
  {
    fn: (url) => parseUrl(url).hostname.endsWith('behance.net'),
    val: 'fab fa-behance',
  },
  {
    fn: (url) => parseUrl(url).hostname.endsWith('blogger.com'),
    val: 'fab fa-blogger',
  },
  {
    fn: (url) => parseUrl(url).hostname.endsWith('bitbucket.org'),
    val: 'fab fa-bitbucket',
  },
  {
    fn: (url) => parseUrl(url).hostname.endsWith('codepen.io'),
    val: 'fab fa-codepen',
  },
  {
    fn: (url) => parseUrl(url).hostname.endsWith('deviantart.com'),
    val: 'fab fa-deviantart',
  },
  {
    fn: (url) => parseUrl(url).hostname.endsWith('discordapp.com'),
    val: 'fa fa-discord',
  },
  {
    fn: (url) => parseUrl(url).hostname.endsWith('dribbble.com'),
    val: 'fab fa-dribbble',
  },
  {
    fn: (url) => parseUrl(url).hostname.endsWith('ello.co'),
    val: 'fab fa-ello',
  },
  {
    fn: (url) => parseUrl(url).hostname.endsWith('etsy.com'),
    val: 'fab fa-etsy',
  },
  {
    fn: (url) => parseUrl(url).hostname.endsWith('facebook.com'),
    val: 'fab fa-facebook',
  },
  {
    fn: (url) => parseUrl(url).hostname.endsWith('github.com'),
    val: 'fab fa-github',
  },
  {
    fn: (url) => parseUrl(url).hostname.endsWith('gitlab.com'),
    val: 'fab fa-gitlab',
  },
  {
    fn: (url) => parseUrl(url).hostname.endsWith('goodreads.com'),
    val: 'fab fa-goodreads',
  },
  {
    fn: (url) => parseUrl(url).hostname.endsWith('instagram.com'),
    val: 'fab fa-instagram',
  },
  {
    fn: (url) => parseUrl(url).hostname.endsWith('keybase.io'),
    val: 'fa fa-keybase',
  },
  {
    fn: (url) => parseUrl(url).hostname.endsWith('kickstarter.com'),
    val: 'fab fa-kickstarter',
  },
  {
    fn: (url) => parseUrl(url).hostname.endsWith('last.fm'),
    val: 'fab fa-lastfm',
  },
  {
    fn: (url) => parseUrl(url).hostname.endsWith('medium.com'),
    val: 'fab fa-medium',
  },
  {
    fn: (url) => parseUrl(url).hostname.endsWith('patreon.com'),
    val: 'fa fa-patreon',
  },
  {
    fn: (url) => parseUrl(url).hostname.endsWith('paypal.com'),
    val: 'fab fa-paypal',
  },
  {
    fn: (url) => parseUrl(url).hostname.endsWith('pinterest.com'),
    val: 'fab fa-pinterest',
  },
  {
    fn: (url) => parseUrl(url).hostname.endsWith('plus.google.com'),
    val: 'fab fa-google-plus-g',
  },
  {
    fn: (url) => parseUrl(url).hostname.endsWith('ravelry.com'),
    val: 'fab fa-ravelry',
  },
  {
    fn: (url) => parseUrl(url).hostname.endsWith('reddit.com'),
    val: 'fab fa-reddit',
  },
  {
    fn: (url) => parseUrl(url).hostname.endsWith('skype.com'),
    val: 'fab fa-skype',
  },
  {
    fn: (url) => parseUrl(url).hostname.endsWith('slack.com'),
    val: 'fab fa-slack',
  },
  {
    fn: (url) => parseUrl(url).hostname.endsWith('snapchat.com'),
    val: 'fab fa-snapchat',
  },
  {
    fn: (url) => parseUrl(url).hostname.endsWith('soundcloud.com'),
    val: 'fab fa-soundcloud',
  },
  {
    fn: (url) => parseUrl(url).hostname.endsWith('stackoverflow.com'),
    val: 'fab fa-stackoverflow',
  },
  {
    fn: (url) => parseUrl(url).hostname.endsWith('steamcommunity.com'),
    val: 'fab fa-steam',
  },
  {
    fn: (url) => parseUrl(url).hostname.endsWith('teamspeak.com'),
    val: 'fab fa-teamspeak',
  },
  {
    fn: (url) => parseUrl(url).hostname.endsWith('tumblr.com'),
    val: 'fab fa-tumblr',
  },
  {
    fn: (url) => parseUrl(url).hostname.endsWith('twitch.tv'),
    val: 'fab fa-twitch',
  },
  {
    fn: (url) => parseUrl(url).hostname.endsWith('twitter.com'),
    val: 'fab fa-twitter',
  },
  {
    fn: (url) => parseUrl(url).hostname.endsWith('untappd.com'),
    val: 'fab fa-untappd',
  },
  {
    fn: (url) => parseUrl(url).hostname.endsWith('vimeo.com'),
    val: 'fab fa-vimeo',
  },
  {
    fn: (url) => parseUrl(url).hostname.endsWith('youtube.com'),
    val: 'fab fa-youtube',
  },

  {
    fn: (url) => parseUrl(url).hostname.includes('pora'),
    val: 'fa fa-diaspora',
  },
  {
    fn: (url) => parseUrl(url).hostname.includes('mastodon'),
    val: 'fa fa-mastodon',
  },

  { fn: (url) => parseUrl(url).protocol === 'mailto:', val: 'fas fa-envelope' },
];

export default iconGuesses;
